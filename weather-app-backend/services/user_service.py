from app.models.user import User
from app.models.city import City
from app.database.database import db
from .city_service import CityService 
from flask import current_app

class UserService:

    @staticmethod
    def find_or_create_user(name):

        # Find user by name (the name is basically a unique key, but not enforced explicitly)        
        user = User.query.filter_by(name=name).first()

        if user:
            return user
        
        # Do not allow more than 100 users to be created
        user_count = User.query.count()
        if user_count >= 100:
            raise Exception("Users limit reached. No more than 100 users are allowed")

        # If we have less than 100 users, create the user and return it        
        user = User(name=name)

        try:

            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            
            db.session.rollback()
            raise Exception("An error occurred while creating the user.")       

        return user
    
    @staticmethod
    def find_user_cities(user_id):

        # Get the cities for a specific user
        user = User.query.get(user_id)

        if not user:
            raise NoResultFound("User not found.")

        return user.cities


    @staticmethod
    def remove_city_from_user(user_id, city_id):

        try:
            # Get the user and city objects
            user = User.query.get(user_id)
            city = City.query.get(city_id)

            if not user:
                raise Exception("User not found")
            
            if not city:
                raise Exception("City not found")

            # Remove from the many-to-many relationship
            user.cities.remove(city)
            
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while removing city: {str(e)}")
    
    @staticmethod
    def add_city(user_id, city_name):

        # Find or create the city
        city = CityService.find_or_create_city(city_name)

        # Get the user by user_id
        user = User.query.get(user_id)
        
        if not user:
            raise Exception("User not found")
        
        # Add city to the user's cities if is not there yet
        if city not in user.cities:

            user.cities.append(city)

            try:
                db.session.commit()
                return {"message": f"City {city.name} added to user {user.name} successfully"}

            except Exception as e:

                db.session.rollback()
                raise Exception(f"Error adding city to user: {str(e)}")
        
        return {"message": "City already added"}