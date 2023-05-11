from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Fact(Base):
    __tablename__ = 'facts'

    id = Column(Integer, primary_key=True)
    category = Column(String)
    fact = Column(String)

    def __str__(self):
        return f"Category: {self.category}, Fact: {self.fact}"
