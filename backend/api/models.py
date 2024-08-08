from sqlalchemy import Column, Integer, String
from .database import Base

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_name = Column(String, index=True, nullable=False)
    school_city = Column(String)
    school_state = Column(String)
    college_board_code = Column(String)
