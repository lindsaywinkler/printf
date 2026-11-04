"""
FastAPI application entry point.
"""

from typing import Annotated

import strawberry
from fastapi import Depends, FastAPI
from model.model import Printer, PrinterStatus
from model.session import get_session
from sqlmodel import Session, select
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title="printf")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/printers")
def list_printers(session: SessionDep) -> list[Printer]:
    return list(session.exec(select(Printer)).all())


class Context(BaseContext):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session


def get_context(session: SessionDep) -> Context:
    return Context(session)


strawberry.enum(PrinterStatus)


@strawberry.type
class PrinterType:
    id: int
    name: str
    highest_resolution: int
    status: PrinterStatus

    @classmethod
    def from_model(cls, printer: Printer) -> "PrinterType":
        return cls(
            id=printer.id,
            name=printer.name,
            highest_resolution=printer.highest_resolution,
            status=printer.status,
        )


@strawberry.type
class Query:
    @strawberry.field
    def printers(self, info: Info[Context, None]) -> list[PrinterType]:
        printers = info.context.session.exec(select(Printer)).all()
        return [PrinterType.from_model(p) for p in printers]

    @strawberry.field
    def printer(self, info: Info[Context, None], id: int) -> PrinterType | None:
        printer = info.context.session.get(Printer, id)
        return PrinterType.from_model(printer) if printer else None


schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema, context_getter=get_context), prefix="/graphql")
