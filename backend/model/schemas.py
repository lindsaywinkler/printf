"""
API request and response models, for validation.
"""

from datetime import UTC, datetime

from pydantic import AwareDatetime, field_validator
from sqlmodel import Field, SQLModel


class PartCreate(SQLModel):
    """A part submitted for printing."""

    name: str = Field(min_length=1)
    required_resolution: int = Field(gt=0, description="Layer height in microns")
    required_material_id: int
    due_time: AwareDatetime = Field(
        description="When the part must be printed, washed and cured by"
    )
    height: float = Field(gt=0, description="Height in mm")
    volume: float = Field(gt=0, description="Volume in cm^3")

    @field_validator("due_time")
    @classmethod
    def due_time_in_future(cls, value: datetime) -> datetime:
        if value <= datetime.now(UTC):
            raise ValueError("due_time must be in the future")
        return value


class PartRead(SQLModel):
    """A part as returned by the API."""

    id: int
    name: str
    required_resolution: int
    required_material_id: int | None
    due_time: datetime
    height: float
    volume: float
    build_id: int | None
