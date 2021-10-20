import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import databases

from app.config import settings


database = databases.Database(settings.database_url)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    settings.database_url
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
