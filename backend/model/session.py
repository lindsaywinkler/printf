"""
Create a session in the database.
"""

import os
from collections.abc import Iterator

from sqlmodel import Session, create_engine

database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
