"""
FastAPI application entry point.
"""

from datetime import datetime
from typing import Annotated

import strawberry
from fastapi import Depends, FastAPI
from model.model import (
    Build,
    Cure,
    Event,
    Job,
    MaintenanceEvent,
    Material,
    Part,
    Printer,
    Wash,
)
from model.session import get_session
from sqlmodel import Session, select
from sqlmodel.sql.sqltypes import AutoString, UTCDateTime
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info
from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyLoader,
    StrawberrySQLAlchemyMapper,
)

# For the purposes of quickly sketching ideas end to end,
# elected to use the strawberry sqlalchemy mapper.
#
# This has many advantages in reducing the amount of boilerplate
# to write. Top level resolvers are written by hand, but
# fields and relationships, as well as batch loading (necessary
# for performance if we have lots of jobs) are taken care of
# automatically.
#
# The tradeoffs are:
# - less control over what fields are exposed (this is part of the advantage
# here - I want new fields to be available as soon as models are edited)
# - more complex query client side
#
# In a production context, I may make a different decision, but
# for the sake of prototyping, this is the fastest way to
# end to end functionality.
mapper = StrawberrySQLAlchemyMapper(
    model_to_type_name=lambda model: f"{model.__name__}Type",
    extra_sqlalchemy_type_to_strawberry_type_map={
        AutoString: str,
        UTCDateTime: datetime,
    },
)

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title="printf")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Not really needed anymore.
# We'd query instead through the GraphQL endpoint, but
# leaving as an example template of the alternative approach
@app.get("/printers")
def list_printers(session: SessionDep) -> list[Printer]:
    return list(session.exec(select(Printer)).all())


class Context(BaseContext):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.sqlalchemy_loader = StrawberrySQLAlchemyLoader(bind=session)


def get_context(session: SessionDep) -> Context:
    return Context(session)


@mapper.type(Printer)
class PrinterType:
    pass


@mapper.type(Material)
class MaterialType:
    pass


@mapper.type(Build)
class BuildType:
    pass


@mapper.type(Job)
class JobType:
    pass


@mapper.type(Part)
class PartType:
    pass


@mapper.type(Cure)
class CureType:
    pass


@mapper.type(Wash)
class WashType:
    pass


@mapper.type(Event)
class EventType:
    pass


@mapper.type(MaintenanceEvent)
class MaintenanceEventType:
    pass


mapper.finalize()


@strawberry.type
class Query:
    @strawberry.field
    def printers(self, info: Info[Context, None]) -> list[PrinterType]:
        return list(info.context.session.exec(select(Printer)).all())

    @strawberry.field
    def printer(self, info: Info[Context, None], id: int) -> PrinterType | None:
        return info.context.session.get(Printer, id)

    @strawberry.field
    def materials(self, info: Info[Context, None]) -> list[MaterialType]:
        return list(info.context.session.exec(select(Material)).all())

    @strawberry.field
    def material(self, info: Info[Context, None], id: int) -> MaterialType | None:
        return info.context.session.get(Material, id)

    @strawberry.field
    def cures(self, info: Info[Context, None]) -> list[CureType]:
        return list(info.context.session.exec(select(Cure)).all())

    @strawberry.field
    def cure(self, info: Info[Context, None], id: int) -> CureType | None:
        return info.context.session.get(Cure, id)

    @strawberry.field
    def washes(self, info: Info[Context, None]) -> list[WashType]:
        return list(info.context.session.exec(select(Wash)).all())

    @strawberry.field
    def wash(self, info: Info[Context, None], id: int) -> WashType | None:
        return info.context.session.get(Wash, id)

    @strawberry.field
    def parts(self, info: Info[Context, None]) -> list[PartType]:
        return list(info.context.session.exec(select(Part)).all())

    @strawberry.field
    def part(self, info: Info[Context, None], id: int) -> PartType | None:
        return info.context.session.get(Part, id)

    @strawberry.field
    def builds(self, info: Info[Context, None]) -> list[BuildType]:
        return list(info.context.session.exec(select(Build)).all())

    @strawberry.field
    def build(self, info: Info[Context, None], id: int) -> BuildType | None:
        return info.context.session.get(Build, id)

    @strawberry.field
    def jobs(self, info: Info[Context, None]) -> list[JobType]:
        return list(info.context.session.exec(select(Job)).all())

    @strawberry.field
    def job(self, info: Info[Context, None], id: int) -> JobType | None:
        return info.context.session.get(Job, id)

    @strawberry.field
    def events(self, info: Info[Context, None]) -> list[EventType]:
        return list(info.context.session.exec(select(Event)).all())

    @strawberry.field
    def event(self, info: Info[Context, None], id: int) -> EventType | None:
        return info.context.session.get(Event, id)

    @strawberry.field
    def maintenance_events(
        self, info: Info[Context, None]
    ) -> list[MaintenanceEventType]:
        return list(info.context.session.exec(select(MaintenanceEvent)).all())

    @strawberry.field
    def maintenance_event(
        self, info: Info[Context, None], id: int
    ) -> MaintenanceEventType | None:
        return info.context.session.get(MaintenanceEvent, id)


schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema, context_getter=get_context), prefix="/graphql")
