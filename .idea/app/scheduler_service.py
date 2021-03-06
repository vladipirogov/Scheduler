from apscheduler.triggers.cron import CronTrigger

from app import repository
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler

socketio = SocketIO(cors_allowed_origins="*")
mqtt = Mqtt()
scheduler = APScheduler()


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
        mqtt.publish('home/command', str(schedule_dict))
        socketio.emit('message', schedule_dict)
        print('job_id: ' + str(id))
    except Exception as e:
        print("job exception: {}".format(repr(e)))
        mqtt.publish('home/command', repr(e))


class Scheduler:

    def __init__(self, apscheduler):
        self.schedules = repository.get_active_schedules()
        self.apscheduler = apscheduler
        self.expression = ''
        self.run_job()

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
