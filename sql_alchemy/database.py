from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("sqlite+pysqlite:///./sql_app.db", echo=True)
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
  metadata=metadata

