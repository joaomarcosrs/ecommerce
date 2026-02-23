from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ecommerce.core.settings import settings

engine = create_engine(settings.DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
