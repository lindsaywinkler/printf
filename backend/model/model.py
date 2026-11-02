"""
Database models are defined here.
"""

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


class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class MaintenanceEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
