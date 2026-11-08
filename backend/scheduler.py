"""
Logic for dealing with submitted parts and having them assigned to builds,
and to all the jobs required for the part to be produced.

There's also functionality here to make sure that builds get sent to
printers on time (but not ahead of time, in case the build can have more
parts added).

Finally, there is helper logic here to calculate print and cure times
for builds, and to derive total production latency implied for each part
(ie. the sum of build and cure times that part has been allocated to).
"""

import math
import uuid
from datetime import UTC, datetime, timedelta

from model.model import Build, BuildStatus, Part
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select


def schedule_part(session: Session, part: Part):
    # Process this part by:
    #
    # - Finding every open build that could accommodate this part by resolution and resin
    # - Filter candidate builds by checking how long this part would take to produce
    #  (print, wash, cure) if added to a candidate build and whether that would push
    # build production time beyond the required completion time of any part in the build
    # - Allocating the part to any of the builds that are available
    # - If no build can accommodate it, create a new build

    # All of the above can be done with a list comprehension:
    # map over builds and parts within builds, with the current part added
    # and add filter condition.

    # Because the properties we need to filter on are
    # computed, we have to load the objects first.

    # Get all pending builds and force eager loading
    # of parts, which we're just about to use
    pending_builds_query = (
        select(Build)
        .where(Build.status == BuildStatus.pending)
        .options(selectinload(Build.parts))
    )
    pending_builds = list(session.exec(pending_builds_query).all())
    candidate_builds = [
        build
        for build in pending_builds
        if build.required_material.id == part.required_material.id
        and build.required_resolution == part.required_resolution
    ]

    # Calculate total build, print and wash time for each candidate
    # and check that adding that sum to the time now
    # remains below this parts target time.
    now = datetime.now(UTC)

    def build_handling_time(build: Build) -> int:
        augmented_parts_list = build.parts + [part]
        print_time = calculate_print_time(session, augmented_parts_list)
        wash_time = calculate_wash_time(session, augmented_parts_list)
        cure_time = calculate_cure_time(session, augmented_parts_list)
        total_handling_time = print_time + wash_time + cure_time
        return total_handling_time

    def build_complete_time(build: Build) -> datetime:
        # When would this build complete if started now
        # and we added the new part to it?
        total_handling_time = build_handling_time(build)
        finish_time = now + timedelta(seconds=total_handling_time)
        return finish_time

    candidate_builds_with_time = [
        (build_complete_time(build), build) for build in candidate_builds
    ]

    viable_builds = [
        build
        for (complete_time, build) in candidate_builds_with_time
        if complete_time < part.due_time
    ]
    # If there is any viable build, use it.
    # Otherwise create a new build.
    if viable_builds:
        target_build = viable_builds[0]
    else:
        target_build = Build(name=f"build-{uuid.uuid4()}", send_by=now)
        session.add(target_build)

    part.build = target_build
    send_by = min([part.due_time for part in target_build.parts]) - timedelta(
        seconds=build_handling_time(target_build)
    )
    target_build.send_by = send_by
    # Then add this part to the new build.
    # The build itself should be responsible for
    # checking that the part can actually be added and
    # must update send_by time.


# Time in seconds
def calculate_print_time(session: Session, parts: list[Part]):
    # Find the max height of parts in the list.  Print time
    # is derived from that.
    max_height = max([part.height for part in parts])

    # Find the number of layers required to print to that
    # height.  Assume layer printing takes a constant 10s.
    # TODO Layer print time ought to be a config variable.
    # TODO Select part safely.
    num_layers = math.ceil(1000 * (max_height / parts[0].required_resolution))
    return num_layers * 10


# Time in seconds
def calculate_wash_time(session: Session, parts: list[Part]):
    # Assuming wash time is a constant ten minutes in the alcohol bath
    # But leaving open the possibility that something needs to
    # be calculated in future.
    #
    # TODO - Wash time ought to be a config variable
    return 60 * 10


# Time in seconds
def calculate_cure_time(session: Session, parts: list[Part]):
    # Cure time is the sum of the volume of all parts
    # multiplied by the time to cure 1cm^3
    # multiplied by the material's curing time factor
    total_volume = sum([part.volume for part in parts])

    # TODO - Base cure time 30s per 1cm^3 but this should be a
    # configurable value.
    # TODO Safe retrieval of part.
    # And we're again completely dependent on the invariant
    # that every part in a build has the same resolution and material.
    return parts[0].required_material.cure_time_factor * total_volume * 30


def check_for_build_submission():
    # Do any builds need to be sent to printers right now?
    # If so, send them and update build status (atomically)
    #
    # This function to be called in a polling loop, started
    # by a FastAPI lifecycle hook (though we ideally only want
    # one - not one per web worker).  Might later want to add
    # a separate scheduler as a pod/container to deployments.
    #
    # Need to think about what needs locking around the whole part
    # submission and build creation process.
    pass
