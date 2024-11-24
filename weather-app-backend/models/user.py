from app.database.database import db

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Many-to-many relationship with City
    cities = db.relationship('City', secondary='user_city', backref='my_cities')
