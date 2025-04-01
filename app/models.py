from sqlalchemy import Column, Integer, String, JSON, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Crypto(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    extra_data = Column(JSON)
    price = Column(Float, unique=False, nullable=True)
