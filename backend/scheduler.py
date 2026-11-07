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

from model.model import (
    Part,
)
from sqlmodel import Session


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
    pass


# TODO Maybe better to pass in the build object rather than the build ID
def calculate_print_time(session: Session, parts: list[Part]):
    pass


def calculate_wash_time(session: Session, parts: list[Part]):
    # This will just be a constant
    pass


def calculate_cure_time(parts: list[Part]):
    pass


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
