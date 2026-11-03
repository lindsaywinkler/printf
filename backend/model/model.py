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


class Printer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    highest_resolution: int  # in microns

    # None when the printer has no material loaded
    current_material_id: int | None = Field(default=None, foreign_key="material.id")
    current_material: Material | None = Relationship()
    status: PrinterStatus = PrinterStatus.offline


class Wash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Cure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Build(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Resolution and material for a build are derived from the parts
    # in the build.  Each time we add a part, we check that the
    # part has the same resolution and material as the parts already
    # in the build.
    parts: list["Part"] = Relationship(back_populates="build")


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


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_ts: datetime
    end_ts: datetime


class MaintenanceEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_id: int = Field(foreign_key="event.id")
