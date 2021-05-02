import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MyTable(Base):
    __tablename__ = 'replied_to'

    comment_id = Column(String, primary_key=True)