"""
Database models are defined here.
"""

from sqlmodel import Field, SQLModel


class Printer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Material(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
