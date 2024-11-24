from flask import Blueprint, request, jsonify, current_app
from ..services.user_service import UserService 

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['POST'])
def find_or_create_user():

    data = request.get_json()
    name = data.get('name')
    # Get user name from the request
    if not name:
      return jsonify({"error": "Name is required"}), 400

    try:
        current_app.logger.debug(f"POST /users")
        # Find or create a user with that name
        user = UserService.find_or_create_user(name)
        # Return the user
        return jsonify({
            "message": "User retrieved successfully",
            "user": {
                "id": user.id,
                "name": user.name,
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_controller.route('/users/<int:user_id>/cities', methods=['GET'])
def get_user_cities(user_id):

    try:
        current_app.logger.debug(f"GET /users/{user_id}/cities")
        # Find cities for specific user
        cities = UserService.find_user_cities(user_id)
        # Map cities model to correct response object
        city_list = [{"id": city.id, "name": city.name, "weather": city.weather, "temp": city.temp} for city in cities]

        return jsonify({"cities": city_list}), 200

    except NoResultFound as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@user_controller.route('/users/<int:user_id>/cities/<int:city_id>', methods=['DELETE'])
def remove_city_from_user(user_id, city_id):

    try:
        current_app.logger.debug(f"DELETE /users/{user_id}/cities/{city_id}")
        # Remove city for specific user
        UserService.remove_city_from_user(user_id, city_id)
        return jsonify({"message": "City removed successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@user_controller.route('/users/<int:user_id>/cities', methods=['POST'])
def add_city_to_user(user_id):
    city_name = request.json.get('cityName')
    
    if not city_name:
        return jsonify({"message": "City name is required"}), 400
    
    try:
        # Add relation between user and city
        current_app.logger.debug(f"POST /users/{user_id}/cities")
        result = UserService.add_city(user_id, city_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500