from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    vendorId = Column(Integer, unique=True, index=True)
    vendor = Column(String)
    name = Column(String)
    mobile = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    visible = Column(Boolean, default=True)