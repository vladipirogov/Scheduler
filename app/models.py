from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


@dataclass
class PlantSchedule(Base):
    __tablename__ = 'plant_schedule'
    id: int
    cronExpression: str
    plantId: int
    activeSchedule: bool
    scheduleName: str
    expired: bool
    dt: str

    id = Column('schedule_id', Integer, primary_key=True)
    cronExpression = Column('cron_expression', String)
    plantId = Column('plant_id', Integer, ForeignKey('plant.id'))
    activeSchedule = Column('active_schedule', Boolean)
    scheduleName = Column('schedule_name', String)
    expired = Column(Boolean)
    plant = relationship("Plant", back_populates="schedules")
    dt = Column('dt', DateTime(timezone=True))


@dataclass
class Plant(Base):
    __tablename__ = 'plant'
    id: int
    name: str
    schedules: PlantSchedule

    id = Column(Integer, primary_key=True)
    name = Column(String)
    schedules = relationship("PlantSchedule", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Plant {}>'.format(self.name)
