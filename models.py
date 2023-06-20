from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransformedData(Base):
    __tablename__ = 'transformed_data'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    sales_amount = Column(Float)

    # Add other columns as needed
