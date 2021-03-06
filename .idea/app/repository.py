from app import models
from app.models import db

from datetime import datetime


def get_all_plants():
    return models.Plant.query.all()


def get_all_schedules():
    return models.PlantSchedule.query.all()


def get_active_schedules():
    return models.PlantSchedule.query.filter_by(activeSchedule=True)


def find_schedule(id):
    return models.PlantSchedule.query.filter_by(id=id).first()


def set_schedule_expired(id):
    models.PlantSchedule\
        .query\
        .filter_by(id=id)\
        .update({"expired": True, "dt": datetime.now()})
    db.session.commit()


def save_model(model):
    db.session.add(model)
    db.session.commit()
    return model.id


def update_model(model):
    db.session.merge(model)
    db.session.commit()


def delete_plant(id):
    db.session.query(models.Plant).filter(models.Plant.id==id).delete()
    db.session.commit()


def delete_schedule(id):
    db.session.query(models.PlantSchedule).filter(models.PlantSchedule.id==id).delete()
    db.session.commit()

