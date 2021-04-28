from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from app.conf import settings

DATABASE_URL = settings.DATABASE_URL = "postgresql://localhost/courstack"

engine = create_engine(DATABASE_URL)

Base = declarative_base()
session_factory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(session_factory)
