from sqlalchemy import Column, Integer, String, JSON, BigInteger
from scripts.db_connector import Base

class LogTable(Base):
    __tablename__ = "log_table"

    reference_number = Column(BigInteger, primary_key=True, index=True)  
    status = Column(String(255))  
    product_names = Column(JSON)  
    image_count = Column(Integer) 