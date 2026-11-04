"""
FastAPI application entry point.
"""

from typing import Annotated

import strawberry
from fastapi import Depends, FastAPI
from model.model import Printer
from model.session import get_session
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title="printf")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/printers")
def list_printers(session: SessionDep) -> list[Printer]:
    return list(session.exec(select(Printer)).all())


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "world"


schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema), prefix="/graphql")
