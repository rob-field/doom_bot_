from sqlalchemy import create_engine, String, Column
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


class MyTable():
    __tablename__ = "replied_to"  # Name of the database table
    # __table_args__ = {'extend_existing': True}  # Specifies that a table with this name already exists in the database

    comment_id = Column(String, primary_key=True)  # Primary key acts as a unique identifier for each database entry

    def __init__(self, comment_id):  # Assigning the appropriate attribute names to each column header of the table
        self.comment_id = comment_id


def db_init():

    Base.metadata.create_all(bind=engine, checkfirst=True)



