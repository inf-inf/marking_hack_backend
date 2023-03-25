from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON

from ..database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer)
    data = Column(JSON, default=True)
    name = Column(String)
