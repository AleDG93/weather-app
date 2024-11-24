from app.models.city import City
from app.database.database import db
from flask import current_app, jsonify
from .weather_city_manager import WeatherCityManager
from datetime import datetime, timedelta

class CityService:

    @staticmethod   
    def find_or_create_city(city_name):

        # Check if the city exists
        city = City.query.filter_by(name=city_name).first()
        
        # If it does, return the city
        if city:
            return city
        
        # Otherwise, create a new city
        new_city = City(name=city_name)

        # Get instance of WeatherCityManager
        weather_manager = WeatherCityManager.get_instance()

        try:
            # Get weather data for the city
            weather_data = weather_manager.get_weather_for_city(city_name)

            # If weather data is returned, update the new city object with the weather data
            if weather_data:

                weather_info = weather_data.get("weather", [{}])[0] 
                main_info = weather_data.get("main", {})
                new_city.weather = weather_info.get("description", "Unknown")
                new_city.temp = main_info.get("temp", 0.0)
                new_city.feels_like = main_info.get("feels_like", 0.0)
                new_city.humidity = main_info.get("humidity", 0)
                new_city.last_call = datetime.now() 

            # Otherwise raise an exception
            else:
                raise Exception(f"Failed to get weather data for city: {city_name}")

            db.session.add(new_city)
            db.session.commit()

            return new_city
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating city: {str(e)}")
    
    @staticmethod
    def get_city(city_id):

        # Find city by ID
        city = City.query.get(city_id)
        if not city:
            raise Exception("City not found")
        
        # Check if last_call is older than 5 minutes
        if city.last_call and datetime.now() - city.last_call > timedelta(minutes=5):

            # If the city data is older than 5 minutes, update the weather data
            weather_manager = WeatherCityManager.get_instance()

            try:
                weather_data = weather_manager.get_weather_for_city(city.name)

                if weather_data:

                    weather_info = weather_data.get("weather", [{}])[0]
                    main_info = weather_data.get("main", {})

                    # Update the city object with the latest weather data
                    city.weather = weather_info.get("description", "Unknown")
                    city.temp = main_info.get("temp", 0.0)
                    city.feels_like = main_info.get("feels_like", 0.0)
                    city.humidity = main_info.get("humidity", 0)
                    city.last_call = datetime.now()

                    db.session.commit()
                    
                else:
                    raise Exception(f"Failed to get weather data for city: {city.name}")

            except Exception as e:
                raise Exception(f"Error updating city weather: {str(e)}")
        
        return city