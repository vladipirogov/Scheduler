from apscheduler.triggers.cron import CronTrigger
import pytz

from app import repository
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from config import Config


jobstores = {
    'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

"""Socketio object"""
socketio = SocketIO(cors_allowed_origins="*")

"""Mqtt ibject"""
mqtt = Mqtt()

"""Scheduler object"""
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.timezone('Europe/Kiev'))



def scheduled_task(id):
    try:
        repository.set_schedule_expired(id)
        schedule = repository.find_schedule(id)
        schedule_dict = {"name": schedule.plant.name,
                         "id": schedule.id,
                         "scheduleName": schedule.scheduleName,
                         "cronExpression": schedule.cronExpression,
                         "plantId": schedule.plantId,
                         "activeSchedule": schedule.activeSchedule,
                         "dt": str(schedule.dt)
                         }
        #mqtt.publish('home/command', str(schedule_dict))
        print(str(schedule_dict))
        socketio.emit('message', schedule_dict)
        print('job_id: ' + str(id))
    except Exception as e:
        print("job exception: {}".format(repr(e)))
        mqtt.publish('home/command', repr(e))


class Scheduler:

    def __init__(self, apscheduler):
        print("scheduler initialization")
        self.schedules = repository.get_active_schedules()
        self.apscheduler = apscheduler
        self.expression = ''
        #self.run_job()

    def run_job(self):
        for schedule in self.schedules:
            self.expression = schedule.cronExpression
            self.apscheduler.add_job(func=scheduled_task,
                                     trigger=CronTrigger.from_crontab(self.expression),
                                     args=[schedule.id],
                                     id=str(schedule.id))
        return 'Scheduled tasks done'

    def add_job(self, id, expression):
        self.apscheduler.add_job(func=scheduled_task,
                                 trigger=CronTrigger.from_crontab(expression),
                                 args=[id],
                                 id=str(id))

    def pause(self):
        self.apscheduler.pause()

    def resume(self):
        self.apscheduler.resume()

    def state(self):
        return self.apscheduler.state()

    def shutdown(self):
        self.apscheduler.shutdown()

    def reschedule(self):
        print("RESCHEDULING")
        self.schedules = repository.get_active_schedules()
        for schedule in self.schedules:
            self.expression = schedule.cronExpression
            print(self.expression)
            self.apscheduler.scheduler.reschedule_job(str(schedule.id),
                                                      trigger=CronTrigger.from_crontab(self.expression))
        print("Scheduler jobs were updated")
        return 'Scheduled tasks done'

    def remove_all_jobs(self):
        self.apscheduler.remove_all_jobs()
