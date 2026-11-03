"""
Database models are defined here.
"""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Printer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Wash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Cure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Material(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Part(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Build(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


# A Job could be a physical job or a computational job.
# A physical job could be print, wash, cure, separate
# A computational job could be recognise, compose, slice
class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_id: int = Field(foreign_key="event.id")


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_ts: datetime
    end_ts: datetime


class MaintenanceEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_id: int = Field(foreign_key="event.id")
