from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    # password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favourite_planets = db.Column(db.String(200))
    favourite_people = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # "email": self.email,
            # do not serialize the password, its a security breach
            "favourite_planets": json.loads(self.favourite_planets),
            "favourite_people": json.loads(self.favourite_people)
        }