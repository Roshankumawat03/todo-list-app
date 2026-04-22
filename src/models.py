from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note = Column(String)
    isDeleted = Column(Boolean, default=False)
    isArchive = Column(Boolean, default=False)
    isPinned = Column(Boolean, default=False)