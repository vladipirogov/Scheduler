from flask import Flask
from config import Config
#from flask_migrate import Migrate
from flask_cors import CORS
#from app.models import db
from app.scheduler_service import scheduler
from app.scheduler_service import mqtt
from app.scheduler_service import socketio
from app.routes import app_route
from app import scheduler_service

# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.register_blueprint(app_route)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.1.107'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_KEEPALIVE'] =20
app.config['MQTT_CLIENT_ID'] = 'org.owl.home'
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True
app.config['CORS_AUTOMATIC_OPTIONS'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

app.config.from_object(Config)
# app.jinja_env.auto_reload = True

mqtt.init_app(app)
mqtt.subscribe("home/#")
# mqtt.init_app(app)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

socketio.init_app(app)

#db.init_app(app)
#migrate = Migrate(app, db)

#scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


