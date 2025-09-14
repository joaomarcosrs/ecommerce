from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ecommerce.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
