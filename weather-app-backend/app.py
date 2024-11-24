from flask import Flask
from flask_cors import CORS
from app.controllers.city_controller import city_controller 
from app.controllers.user_controller import user_controller 
from app.database.database import db, init_app
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@host.docker.internal:5432/weather-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV'] = 'development'

app.logger.setLevel(logging.DEBUG)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE"]}})

init_app(app)

app.register_blueprint(city_controller)
app.register_blueprint(user_controller)

if __name__ == '__main__':
    app.run(debug=True)