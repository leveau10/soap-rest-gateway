from database import Base, engine
from sqlalchemy import Column, Integer, String


class Time(Base):
    __tablename__ = "times_time"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cidade = Column(String, index=True)
    estado = Column(String, index=True)

Base.metadata.create_all(bind=engine)