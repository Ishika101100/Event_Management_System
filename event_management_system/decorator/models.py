from flask_login import current_user
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import backref

from event_management_system import db


class Decorator(db.Model):
    """add decorator in the database"""
    __tablename__ = "decorator"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    decoration_type = db.relationship("DecoratorGetTypes", backref='decorator_get_types', lazy=True)
    venues = db.relationship("VenueGetDecorator", backref=backref("venue_get_decorators", uselist=False))
    event = db.relationship('Event', backref=backref("decorator_get_events", uselist=False))
    user = db.relationship('User', backref=backref("User", uselist=False))


class DecoratorType(db.Model):
    """add decoration type in the database"""
    __tablename__ = "decorator_type"
    id = db.Column(db.Integer, primary_key=True)
    decoration_type = db.Column(db.String)
    decorator = db.relationship("DecoratorGetTypes", backref='decorator_get_decorationType', lazy=True)

    def __repr__(self):
        return self.id


class DecoratorGetTypes(db.Model):
    """mapping table of decorator and decoration types"""
    __tablename__ = "decorator_get_types"
    __table_args__ = (
        PrimaryKeyConstraint('decorator_id', 'decoration_type_id'),
    )
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    decoration_type_id = db.Column(db.Integer, db.ForeignKey('decorator_type.id'))
    charges = db.Column(db.Integer)


def save_decorator(user_id):
    decorator = Decorator(user_id=user_id)
    db.session.add(decorator)
    db.session.commit()
    return decorator


def get_decorator_for_venue(user_id):
    return Decorator.query.filter_by(user_id=user_id).first()


def get_current_decorator():
    return Decorator.query.filter_by(user_id=current_user.id).first()


def get_decor_category(decoration_type):
    return DecoratorType(decoration_type=decoration_type)


def decor_get_types(decorator_id, decoration_type_id, charges):
    return DecoratorGetTypes(decorator_id=decorator_id, decoration_type_id=decoration_type_id,
                             charges=charges)


def get_decor_charges(decorator_id, decoration_type_id):
    return DecoratorGetTypes.query.filter_by(decorator_id=decorator_id, decoration_type_id=decoration_type_id).first()


def get_decoration_category(decorator_type_id):
    return DecoratorType.query.filter_by(id=decorator_type_id).first()


def get_decorator_type(decorator_id):
    return DecoratorGetTypes.query.filter_by(decorator_id=decorator_id).all()
