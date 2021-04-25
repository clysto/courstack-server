from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.conf import settings

DATABASE_URL = settings.DATABASE_URL = "postgresql://localhost/courstack"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
