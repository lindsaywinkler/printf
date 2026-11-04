"""
Idempotent database seed script.

Just adds a few printers and a few different resins that we can work
with, so that we have some kind of test print farm set up to work with.
"""

from model.model import Material, Printer, PrinterStatus
from model.session import engine
from sqlmodel import Session, select


def safe_create(session: Session, model, name: str, **fields):
    """
    Important to check whether the DB already has this entity in it
    so that we don't create dupes.
    """
    existing = session.exec(select(model).where(model.name == name)).first()
    if existing:
        return existing
    obj = model(name=name, **fields)
    session.add(obj)
    return obj


def main() -> None:
    with Session(engine) as session:
        grey = safe_create(session, Material, "grey_resin")
        clear = safe_create(session, Material, "clear_resin")

        safe_create(
            session,
            Printer,
            "printer_01",
            highest_resolution=25,
            status=PrinterStatus.ready,
            current_material=grey,
        )
        safe_create(
            session,
            Printer,
            "printer_02",
            highest_resolution=50,
            status=PrinterStatus.printing,
            current_material=clear,
        )
        safe_create(
            session,
            Printer,
            "printer_03",
            highest_resolution=25,
            status=PrinterStatus.no_resin,
        )
        safe_create(
            session,
            Printer,
            "printer_04",
            highest_resolution=100,
            status=PrinterStatus.breakdown,
            current_material=grey,
        )

        session.commit()


if __name__ == "__main__":
    main()
