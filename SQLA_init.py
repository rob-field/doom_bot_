from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(uri, convert_unicode=True)  # Creating an engine object to connect to the database
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))  # Creating a session object to provide access when querying the database

Base = declarative_base()  # A base class that can be used to declare class definitions which define the database tables
# Base.query = db_session.query_property()


def init_db():
    """
    Initialising the database
    """
    from models import MyTable  # importing required modules to be registered on the metadata

    MyTable.__table__.create(bind=engine, checkfirst=True)

    Base.metadata.create_all(bind=engine)  # Create the database tables