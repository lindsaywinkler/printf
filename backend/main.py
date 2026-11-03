"""
FastAPI application entry point.
"""

from typing import Annotated

from fastapi import Depends, FastAPI
from model.model import Printer
from model.session import get_session
from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title="printf")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/printers")
def list_printers(session: SessionDep) -> list[Printer]:
    return list(session.exec(select(Printer)).all())
