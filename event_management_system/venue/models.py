from flask import request
from flask_login import current_user
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref

from event_management_system import db
from event_management_system.book_event.models import EventCategory
from event_management_system.caterer.models import Caterer
from event_management_system.decorator.models import Decorator


class Venues(db.Model):
    """add venues in the database"""
    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    decorator = relationship('VenueGetDecorator', backref='decorator_get_venue', lazy=True)
    caterer = relationship("VenueGetCaterer", backref='caterer_get_venue', lazy=True)
    event = relationship("Event", backref='venue_get_event', cascade="all, delete-orphan", lazy="joined")
    venue_type = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    charges = db.Column(db.Integer)
    user = db.relationship('User', backref=backref("User_for_venue", uselist=False))


class VenueGetDecorator(db.Model):
    """mapping table of venue and decorator"""
    __tablename__ = "venue_get_decorator"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'decorator_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    is_approved_decorator = db.Column(db.Boolean)


class VenueGetCaterer(db.Model):
    """mapping table of venue and caterer"""
    __tablename__ = "venue_get_caterer"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'caterer_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    is_approved_caterer = db.Column(db.Boolean)


def save_venue(user_id):
    venue = Venues(venue_type=request.form.get('event_category'), capacity=request.form.get('event_capacity'),
                   charges=request.form.get('event_charges'), user_id=user_id)
    db.session.add(venue)
    db.session.commit()
    return venue


def get_all_venues():
    return Venues.query.all()


def get_current_venue():
    return Venues.query.filter_by(user_id=current_user.id).first()


def venue_get_decorator_query_for_decorator(decorator_id, is_approved_decorator):
    return VenueGetDecorator.query.filter_by(decorator_id=decorator_id).filter_by(
        is_approved_decorator=is_approved_decorator).with_entities(VenueGetDecorator.venue_id,
                                                                   VenueGetDecorator.is_approved_decorator).all()


def get_venue_get_decorator_obj_for_decorator(venue_id, decorator_id):
    return VenueGetDecorator(venue_id=venue_id, decorator_id=decorator_id)


def get_venue(venue_user_id):
    return Venues.query.filter(venue_user_id == Venues.user_id).first()


def get_venue_get_decorator_obj(is_approved_decorator_by_venue):
    return VenueGetDecorator.query.join(Decorator, VenueGetDecorator.decorator_id == Decorator.id).join(
        Venues, VenueGetDecorator.venue_id == Venues.id).add_columns(Decorator.user_id).filter(
        VenueGetDecorator.decorator_id == Decorator.id).filter(Venues.user_id == current_user.id).filter(
        VenueGetDecorator.venue_id == Venues.id).filter(
        VenueGetDecorator.is_approved_decorator == is_approved_decorator_by_venue).all()


def get_venue_get_decorator_query(venue_object, decorator_id):
    return VenueGetDecorator.query.filter_by(venue_id=venue_object, decorator_id=decorator_id).first()


def get_venue_get_caterer_obj(is_approved_caterer_by_venue):
    return VenueGetCaterer.query.join(Caterer, VenueGetCaterer.caterer_id == Caterer.id).add_columns(
        Caterer.user_id).filter(VenueGetCaterer.caterer_id == Caterer.id).filter(
        VenueGetCaterer.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
        VenueGetCaterer.is_approved_caterer == is_approved_caterer_by_venue).all()


def get_venue_caterer_query(venue, caterer_id):
    return VenueGetCaterer.query.filter_by(venue_id=venue, caterer_id=caterer_id).first()


def venue_get_caterer_obj_for_caterer(caterer_id, is_approved_caterer):
    return VenueGetCaterer.query.filter_by(caterer_id=caterer_id).filter_by(
        is_approved_caterer=is_approved_caterer).with_entities(VenueGetCaterer.venue_id,
                                                               VenueGetCaterer.is_approved_caterer).all()


def venue_get_caterer_query(venue_id, caterer_id):
    return VenueGetCaterer(venue_id=venue_id, caterer_id=caterer_id)


def get_venue_for_event(event_type_id):
    return Venues.query.join(EventCategory, Venues.venue_type == event_type_id).filter(
        Venues.venue_type == EventCategory.id).all()


def get_venue_data_for_event(venue_id):
    return Venues.query.filter_by(id=venue_id).first()


def venue_get_caterer_for_event(venue_id):
    return VenueGetCaterer.query.join(Caterer, VenueGetCaterer.caterer_id == Caterer.id).filter(
        VenueGetCaterer.caterer_id == Caterer.id).filter(VenueGetCaterer.venue_id == venue_id).filter(
        VenueGetCaterer.is_approved_caterer == True).all()


def caterer_query_for_event(caterer_id):
    return VenueGetCaterer.query.filter_by(caterer_id=caterer_id).first()


def venue_get_decorator_for_event(venue_id):
    return VenueGetDecorator.query.join(Decorator, VenueGetDecorator.decorator_id == Decorator.id).filter(
        VenueGetDecorator.decorator_id == Decorator.id).filter(VenueGetDecorator.venue_id == venue_id).filter(
        VenueGetDecorator.is_approved_decorator == True).all()


def decorator_query_for_event(decorator_id):
    return VenueGetDecorator.query.filter_by(decorator_id=decorator_id).first()


def book_event_get_venue_query():
    return Venues.query.join(EventCategory, Venues.venue_type == EventCategory.id).filter(
        Venues.venue_type == EventCategory.id).all()


def get_caterer_query_for_event():
    return VenueGetCaterer.query.join(Caterer, VenueGetCaterer.caterer_id == Caterer.id).filter(
        VenueGetCaterer.caterer_id == Caterer.id).all()


def get_decorator_for_event():
    return VenueGetDecorator.query.join(Decorator, VenueGetDecorator.decorator_id == Decorator.id).filter(
        VenueGetDecorator.decorator_id == Decorator.id).all()
