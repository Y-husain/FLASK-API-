from app import db
from app.models.user_models import User


class Category(db.Model):
    """ORM that store recipe category"""
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name, detail):
        self.name = name
        self.detail = detail

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):  # pragma: no cover
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Categories:{}>".format(self.name)
