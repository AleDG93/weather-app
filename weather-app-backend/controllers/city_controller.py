from flask import Blueprint, request, jsonify, current_app
from ..services.city_service import CityService 

city_controller = Blueprint('city_controller', __name__)


@city_controller.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    current_app.logger.debug(f"GET /cities/{city_id}")
    # Find city by ID
    city = CityService.get_city(city_id)
    if city:
        return jsonify(
            {
                "id": city.id, 
                "name": city.name,    
                "weather": city.weather,
                "temp": city.temp,
                "feelsLike": city.feels_like,
                "humidity": city.humidity,
                "lastCall": city.last_call
        }), 200
    return jsonify({"message": "City not found"}), 404
