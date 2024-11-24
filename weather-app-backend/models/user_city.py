from app.database.database import db

class UserCity(db.Model):
    
    __tablename__ = 'user_city'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), primary_key=True)