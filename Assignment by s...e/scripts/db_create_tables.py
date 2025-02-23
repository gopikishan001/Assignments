from scripts.db_connector import engine
from scripts.db_connector import Base

Base.metadata.create_all(bind=engine)
