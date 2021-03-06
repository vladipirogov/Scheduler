from app import models
from app.database import Session
from app.models import PlantSchedule, Plant

from datetime import datetime


def get_all_plants():
    return Session.query(Plant).all()


def get_all_schedules():
    return Session.query(PlantSchedule).all()


def get_active_schedules():
    return Session.query(PlantSchedule).filter_by(activeSchedule=True)


def find_schedule(id):
    return Session.query(PlantSchedule).filter_by(id=id).first()


def set_schedule_expired(id):
    Session.query(PlantSchedule).filter_by(id=id)\
        .update({"expired": True, "dt": datetime.now()})
    Session.commit()


def save_model(model):
    Session.add(model)
    Session.commit()
    return model.id


def update_model(model):
    Session.merge(model)
    Session.commit()


def delete_plant(id):
    Session.query(models.Plant).filter(models.Plant.id==id).delete()
    Session.commit()


def delete_schedule(id):
    Session.query(models.PlantSchedule).filter(models.PlantSchedule.id==id).delete()
    Session.commit()

