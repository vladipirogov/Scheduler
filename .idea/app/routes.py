from flask import request
from flask import jsonify
from flask import Blueprint
from app import repository
from apscheduler.triggers.cron import CronTrigger
from app.scheduler_service import mqtt
from app.scheduler_service import Scheduler as cron_scheduler
from app.scheduler_service import scheduler

app_route = Blueprint('app_route', __name__)


switcher = {
    "home/scheduler/get_jobs": lambda: mqtt.publish("scheduler/response", str(scheduler.get_jobs())),
    "home/scheduler/reschedule": lambda: cron_scheduler.reschedule()
}


def message_received():
    print('message was received!!!')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('on_connect client : {} userdata :{} flags :{} rc:{}'.format(client, userdata, flags, rc))
    mqtt.subscribe("test/plants")


@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('on_subscribe client : {} userdata :{} mid :{} granted_qos:{}'.format(client, userdata, mid, granted_qos))


@mqtt.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("client: {}, userdata: {}, rc: {}".format(client, userdata, rc))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("client: {}, userdata: {}, topic: {}, payload: {}".format(client, userdata, message.topic, message.payload.decode()))
    try:
        switcher.get(message.topic)()
    except Exception:
        print("job exception")
        mqtt.publish('scheduler/response', "EXCEPTION")


@app_route.route('/plants', methods=['GET'])
def get_all_plants():
    plants = repository.get_all_plants()
    return jsonify(plants)


@app_route.route('/schedules', methods=['GET'])
def get_all_schedules():
    schedules = repository.get_all_schedules()
    return jsonify(schedules)


@app_route.route('/plants/plant', methods=['PUT', 'POST', 'DELETE'])
def save_plant():
    plant = request.get_json()

    if request.method == 'POST':
        plant_model = repository.models.Plant(name=plant['name'])
        repository.save_model(plant_model)

    if request.method == 'PUT':
        plant_model = repository.models.Plant(id=plant['id'], name=plant['name'])
        repository.update_model(plant_model)

    if request.method == 'DELETE':
        id = plant['id']
        repository.delete_plant(id)

    return jsonify(plant)


@app_route.route('/plants/schedule', methods=['DELETE'])
def delete_schedule():
    schedule = request.get_json()
    print("Deleting schedule!")
    id = schedule['id']
    print("id = " + str(id))
    repository.delete_schedule(id)
    job_state = scheduler.get_job(id=str(id))
    print(job_state)
    if job_state is not None:
        scheduler.remove_job(str(id))
    return jsonify(schedule)


@app_route.route('/plants/schedule', methods=['PUT'])
def save_schedule():
    schedule = request.get_json()

    schedule_model = repository.models.PlantSchedule(
        id=schedule['id'],
        cronExpression=schedule['cronExpression'],
        activeSchedule=schedule['activeSchedule'],
        scheduleName=schedule['scheduleName'],
        expired=schedule['expired'],
        dt=schedule['dt']
    )

    repository.update_model(schedule_model)

    model_trigger = CronTrigger.from_crontab(schedule_model.cronExpression)
    job = scheduler.get_job(str(schedule_model.id))

    if job is not None and job.id == str(schedule_model.id):  # if job with id exists in the OWL
        print("Job with id exists in the OWL")
        print(job)
        if schedule_model.activeSchedule:  # if the requested schedule is active
            if str(job.trigger) != str(model_trigger):
                print("Reschedule job")
                scheduler.scheduler.reschedule_job(job.id, trigger=model_trigger)
        else:
            print("The job is going to be deleted!")
            scheduler.remove_job(job.id)
    else:
        print("The job is missing in the OWL")
        if schedule_model.activeSchedule:
            print("The job is going to be added to OWL")
            cron_scheduler.add_job(schedule_model.id, schedule_model.cronExpression)

    return jsonify(schedule_model)


@app_route.route('/plants/schedule', methods=['POST'])
def post_schedule():
    schedule = request.get_json()

    schedule_model = repository.models.PlantSchedule(
        cronExpression=schedule['cronExpression'],
        activeSchedule=schedule['activeSchedule'],
        scheduleName=schedule['scheduleName'],
        plantId=schedule['plantId'],
        expired=schedule['expired']
    )
    id = repository.save_model(schedule_model)
    print("post id: " + str(id))
    if schedule_model.activeSchedule:
        cron_scheduler.add_job(id, schedule_model.cronExpression)
    return jsonify(schedule_model)


@app_route.route('/job', methods=['GET'])
def get_state():
    job_id = request.args.get('id')
    print("id: " + job_id)
    job_state = scheduler.get_job(id=job_id)
    print(job_state)
    return jsonify(str(job_state))

