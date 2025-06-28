from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataEntry(Base):
    __tablename__ = "data_entries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    meta = Column(String)
    vector = Column(LargeBinary)  # Combined id+name vector
    id_vector = Column(LargeBinary)  # ID-only vector
    name_vector = Column(LargeBinary)  # Name-only vector 