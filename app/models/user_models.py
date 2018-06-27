from datetime import datetime
from flask_bcrypt import Bcrypt
from app import db


class User(db.Model):
    """ User  details table"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')
        self.registered_on = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):  # pragma: no cover
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User:{}>".format(self.first_name)