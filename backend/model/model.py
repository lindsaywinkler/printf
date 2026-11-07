"""
Database models are defined here.
"""

from datetime import datetime
from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel


class PrinterStatus(StrEnum):
    ready = "ready"
    offline = "offline"
    breakdown = "breakdown"
    no_resin = "no_resin"
    printing = "printing"


class Material(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # The time it takes a particular volume of resin
    # to cure will also be dependent on the properties
    # of the resin itself.  This is a multiplier on
    # the resin volume to give required cure time.
    #
    # In the real world, the geometry of the shape
    # would mattter too.
    cure_time_factor: float


class Printer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    highest_resolution: int  # in microns

    # None when the printer has no material loaded
    current_material_id: int | None = Field(default=None, foreign_key="material.id")
    current_material: Material | None = Relationship()
    status: PrinterStatus = PrinterStatus.offline


class WashStatus(StrEnum):
    ready = "ready"
    offline = "offline"
    breakdown = "breakdown"
    no_alcohol = "no_alcohol"
    washing = "washing"


# Wash is a machine, probably poorly named.
# But this model is to model the wash station.
class Wash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: WashStatus = WashStatus.offline


class CureStatus(StrEnum):
    ready = "ready"
    offline = "offline"
    breakdown = "breakdown"
    curing = "curing"


# Cure is the curing station - a machine. Poorly named.
class Cure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: CureStatus = CureStatus.offline


class BuildStatus(StrEnum):
    pending = "pending"
    printing = "printing"
    washing = "washing"
    curing = "curing"
    done = "done"


class Build(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Resolution and material for a build are derived from the parts
    # in the build.  Each time we add a part, we check that the
    # part has the same resolution and material as the parts already
    # in the build.
    parts: list["Part"] = Relationship(back_populates="build")

    # TODO - Add calculated field which determines print time
    # according to height of the build, which is the height of the
    # tallest part in the build.

    # TODO - Add calculated field which determines cure time
    # according to sum of volume of all parts and a cure
    # factor for the resin/material itself.
    status: BuildStatus = BuildStatus.pending

    # send_by is the time by which this build should be sent to
    # the printer to ensure that every job (print, wash, cure) can
    # be completed by the soonest required time for every part in
    # the build.
    send_by: datetime


class Part(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # A part can exist on its own, or it can be grouped into a build
    # ie. a part belongs to zero or one builds
    name: str

    build_id: int | None = Field(default=None, foreign_key="build.id", index=True)
    build: Build | None = Relationship(back_populates="parts")
    required_resolution: int  # in microns
    required_material_id: int | None = Field(default=None, foreign_key="material.id")
    required_material: Material | None = Relationship()

    # Intended to capture the idea that this part
    # must be ready to ship by this time.  This is to
    # allow addition of a lag time where the part can
    # be held until enough matching parts are available
    # to construct a sensible build.
    #
    # Note that all handling of the part must be complete by this
    # time: printed, washed and cured.
    due_time: datetime

    # Height in mm, which will be converted to microns when
    # calculating build print time.
    #
    # In the real world, parts would be rotated according to their
    # geometry in order to give both a physically stable print and
    # to minimise print time, but for simplicity of demo, we just
    # specify assumed part height directly.
    #
    # mm maybe a poor choice because not an SI unit, but
    # likely most natural unit for a user to specify
    height: float

    # Volume in cm^3.  Again, not an SI unit, but probably
    # the most natural way for a user to think of volume.
    #
    # Volume is required because the cure time will be derived
    # from volume and material (Elsey's two potato problem)
    volume: float


# A Job could be a physical job or a computational job.
# A physical job could be print, wash, cure, separate
# A computational job could be recognise, compose, slice
class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_id: int = Field(foreign_key="event.id")

    # Physical jobs operate on builds
    # We print the whole build, or wash it, cure it, or separate into parts
    build_id: int | None = Field(default=None, foreign_key="build.id", index=True)
    build: Build | None = Relationship()

    # TODO - Add expected duration, which will come from the build
    # This will feed into scheduling: given a start time and duration,
    # we can derive completion time.
    #
    # Note that wash and cure jobs will be independent of build
    # vertical height but curing time will depend on printed volume
    # and the resin in the real world.


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_ts: datetime
    end_ts: datetime


class MaintenanceEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_id: int = Field(foreign_key="event.id")
