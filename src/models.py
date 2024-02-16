from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class States(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    postal_code = db.Column(db.Integer,unique = True, nullable = False)

    def __repr__(self):
        return '<States %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code
        }

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    postal_code = db.Column(db.Integer, db.ForeignKey('states.postal_code'), unique = False, nullable = False)
    states = db.relationship(States)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "postal_code": self.postal_code
        }
    

    