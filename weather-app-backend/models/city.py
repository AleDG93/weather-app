from app.database.database import db
from app.models.user import User
from app.models.user_city import UserCity

class City(db.Model):
    
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    last_call = db.Column(db.Date, nullable=False)

    # Many-to-many relationship with User
    user_cities = db.relationship('User', secondary='user_city', backref='my_users')

    def __repr__(self):
        return f'<City {self.name}>'
