from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class PlantSchedule(db.Model):
    db.__tablename__ = 'plant_schedule'
    id: int
    cronExpression: str
    plantId: int
    activeSchedule: bool
    scheduleName: str
    expired: bool
    dt: str

    id = db.Column('schedule_id', db.Integer, primary_key=True)
    cronExpression = db.Column('cron_expression', db.String)
    plantId = db.Column('plant_id', db.Integer, db.ForeignKey('plant.id'))
    activeSchedule = db.Column('active_schedule', db.Boolean)
    scheduleName = db.Column('schedule_name', db.String)
    expired = db.Column(db.Boolean)
    plant = db.relationship("Plant", back_populates="schedules")
    dt = db.Column('dt', db.DateTime(timezone=True))


@dataclass
class Plant(db.Model):
    db.__tablename__ = 'plant'
    id: int
    name: str
    schedules: PlantSchedule

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    schedules = db.relationship("PlantSchedule", cascade="all, delete-orphan")

    def __repr__(self):
        return '<Plant {}>'.format(self.name)
