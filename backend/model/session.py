"""
Create a session in the database.
"""

from sqlmodel import create_engine

database_url = ""
engine = create_engine()
