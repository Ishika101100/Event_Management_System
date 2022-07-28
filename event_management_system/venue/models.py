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

    @staticmethod
    def add_function(value):
        """function to add data in database"""
        db.session.add(value)

    @staticmethod
    def delete_function(value):
        """function to delete data in database"""
        db.session.delete(value)

    @staticmethod
    def commit_function():
        """function to commit data in database"""
        db.session.commit()

    @classmethod
    def save_venue(cls, user_id):
        """
        save current user as venue
        :param user_id:from current user's id
        :return:save venue details in venue table
        """
        venue = cls(venue_type=request.form.get('event_category'), capacity=request.form.get('event_capacity'),
                    charges=request.form.get('event_charges'), user_id=user_id)
        db.session.add(venue)
        db.session.commit()
        return True

    @staticmethod
    def get_all_venues():
        """
        get list of all venues in venue table
        :return: venue query
        """
        return Venues.query.all()

    @classmethod
    def get_current_venue(cls):
        """
        get venue details for current user
        :return: venue table query if user_id is same as current user's id
        """
        return cls.query.filter_by(user_id=current_user.id).first()

    @classmethod
    def update_venue_info(cls, venue_charge, venue_capacity):
        """
        venue can update its information such as venue capacity and charge
        :param venue_charge: from the update venue info form
        :param venue_capacity: from the update venue info form
        :return: saving venue's updated details
        """
        venue = cls.get_current_venue()
        venue.charges = venue_charge
        venue.capacity = venue_capacity
        cls.commit_function()

    @classmethod
    def get_venue(cls, venue_user_id):
        """
        getting venue information for updating details
        :param venue_user_id:from venue.user_id
        :return:Venue query by filtering venue_user_id
        """
        return cls.query.filter(venue_user_id == cls.user_id).first()

    @classmethod
    def get_venue_for_event(cls, event_type_id):
        """
        venue query for event
        :param event_type_id:from EventCategory table
        :return: Venue query by joining EventCategory table and filtering it by venue_type==EventCategory id
        """
        return cls.query.join(EventCategory, cls.venue_type == event_type_id).filter(
            cls.venue_type == EventCategory.id).all()

    @classmethod
    def get_venue_data_for_event(cls, venue_id):
        """
        venue query for event
        :param venue_id: from current user's id
        :return: venue query by filtering id = venue id
        """
        return cls.query.filter_by(id=venue_id).first()

    @classmethod
    def book_event_get_venue_query(cls):
        """
        venue query for event
        :return: Venue query by joining EventCategory table and filtering it by venue_type==EventCategory id
        """
        return cls.query.join(EventCategory, cls.venue_type == EventCategory.id).filter(
            cls.venue_type == EventCategory.id).all()


class VenueGetDecorator(db.Model):
    """mapping table of venue and decorator"""
    __tablename__ = "venue_get_decorator"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'decorator_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    is_approved_decorator = db.Column(db.Boolean)

    @staticmethod
    def add_function(value):
        """function to add data in database"""
        db.session.add(value)

    @staticmethod
    def delete_function(value):
        """function to delete data in database"""
        db.session.delete(value)

    @staticmethod
    def commit_function():
        """function to commit data in database"""
        db.session.commit()

    @classmethod
    def venue_get_decorator_query_for_decorator(cls, decorator_id, is_approved_decorator):
        """
        VenueGetDecorator query for getting decorator details
        :param decorator_id: from current_user's id
        :param is_approved_decorator: status provided by venue
        :return: VenueGetDecorator query by filtering decorator_id and venue approval
        """
        return cls.query.filter_by(decorator_id=decorator_id).filter_by(
            is_approved_decorator=is_approved_decorator).with_entities(cls.venue_id,
                                                                       cls.is_approved_decorator).all()

    @classmethod
    def get_venue_get_decorator_obj_for_decorator(cls, venue_id, decorator_id):
        """
        Venue details for decorator
        :param venue_id:from selected venue form the given venue list
        :param decorator_id:from current_user's id
        :return:adding venue and decorator details to VenueGetDecorator table
        """
        venue_decorator_obj = cls(venue_id=venue_id, decorator_id=decorator_id)
        cls.add_function(venue_decorator_obj)
        cls.commit_function()

    @classmethod
    def get_venue_get_decorator_obj(cls, is_approved_decorator_by_venue):
        """
        Getting Venue and decorator details form VenueGetDecorator table
        :param is_approved_decorator_by_venue:from VenueGetDecorator table
        :return:VenueGetDecorator query by joining venue and decorator table
        """
        return cls.query.join(Decorator, cls.decorator_id == Decorator.id).join(
            Venues, cls.venue_id == Venues.id).add_columns(Decorator.user_id).filter(
            cls.decorator_id == Decorator.id).filter(Venues.user_id == current_user.id).filter(
            cls.venue_id == Venues.id).filter(
            cls.is_approved_decorator == is_approved_decorator_by_venue).all()

    @classmethod
    def get_venue_get_decorator_query(cls, venue_object, decorator_id):
        """
        Venue get decorator query for getting venue and decorator details
        :param venue_object: from current_user's id
        :param decorator_id: from VenueGetDecorator table
        :return: VenueGetDecorator query by filtering venue_id and decorator_id
        """
        return cls.query.filter_by(venue_id=venue_object, decorator_id=decorator_id).first()

    @classmethod
    def venue_get_decorator_for_event(cls, venue_id):
        """
        Venue and decorator details for booking event
        :param venue_id:from current_user's id
        :return:VenueGetDecorator query by joining Decorator table
        """
        return cls.query.join(Decorator, cls.decorator_id == Decorator.id).filter(
            cls.decorator_id == Decorator.id).filter(cls.venue_id == venue_id).filter(
            cls.is_approved_decorator == True).all()

    @classmethod
    def get_approval_from_venue(cls, venue_obj_id, decorator_id, is_approved_decorator):
        """
        decorator requests venue for business deal
        :param venue_obj_id: from list of venues available
        :param decorator_id: from current user's id
        :param is_approved_decorator: from VenueGetDecorator table
        :return: change is_approved_decorator value in VenueGetDecorator table
        """
        venue_get_decorator_obj = cls.get_venue_get_decorator_query(venue_obj_id, decorator_id)
        venue_get_decorator_obj.is_approved_decorator = is_approved_decorator
        cls.commit_function()

    @classmethod
    def decorator_query_for_event(cls, decorator_id):
        """
        list of events where decorator has decorated the venue
        :param decorator_id:
        :return:
        """
        return cls.query.filter_by(decorator_id=decorator_id).first()

    @classmethod
    def get_decorator_for_event(cls):
        """ user get list of decorator for booking event"""
        return cls.query.join(Decorator, cls.decorator_id == Decorator.id).filter(
            cls.decorator_id == Decorator.id).all()


class VenueGetCaterer(db.Model):
    """mapping table of venue and caterer"""
    __tablename__ = "venue_get_caterer"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'caterer_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    is_approved_caterer = db.Column(db.Boolean)

    @staticmethod
    def add_function(value):
        """function to add data in database"""
        db.session.add(value)

    @staticmethod
    def delete_function(value):
        """function to delete data in database"""
        db.session.delete(value)

    @staticmethod
    def commit_function():
        """function to commit data in database"""
        db.session.commit()

    @classmethod
    def get_venue_get_caterer_obj(cls, is_approved_caterer_by_venue):
        """
        VenueGetCaterer query for getting caterer details
        :param is_approved_caterer_by_venue: status provided by venue
        :return: VenueGetCaterer query by filtering caterer_id and venue approval
        """
        return cls.query.join(Caterer, cls.caterer_id == Caterer.id).add_columns(
            Caterer.user_id).filter(cls.caterer_id == Caterer.id).filter(
            cls.venue_id == Venues.id).filter(Venues.user_id == current_user.id).filter(
            cls.is_approved_caterer == is_approved_caterer_by_venue).all()

    @classmethod
    def get_venue_caterer_query(cls, venue, caterer_id):
        """VenueGetCaterer query for getting venue and caterer details"""
        return cls.query.filter_by(venue_id=venue, caterer_id=caterer_id).first()

    @classmethod
    def venue_get_caterer_obj_for_caterer(cls, caterer_id, is_approved_caterer):
        """VenueGetCaterer query for getting venue and caterer details by filtering is_approved_caterer value"""
        return cls.query.filter_by(caterer_id=caterer_id).filter_by(
            is_approved_caterer=is_approved_caterer).with_entities(cls.venue_id,
                                                                   cls.is_approved_caterer).all()

    @classmethod
    def venue_get_caterer_query(cls, venue_id, caterer_id):
        """VenueGetCaterer query for getting venue and caterer details"""
        venue_caterer_obj = cls(venue_id=venue_id, caterer_id=caterer_id)
        cls.add_function(venue_caterer_obj)
        cls.commit_function()

    @classmethod
    def caterer_get_approval_from_venue(cls, venue_obj_id, caterer_id, is_approved_caterer):
        """
        caterer requests venue for business deal
        :param venue_obj_id: from list of venues available
        :param caterer_id: from current user's id
        :param is_approved_caterer: from VenueGetCaterer table
        :return: change is_approved_caterer value in VenueGetCaterer table
        """
        venue_get_caterer_obj = VenueGetCaterer.get_venue_caterer_query(venue_obj_id, caterer_id)
        venue_get_caterer_obj.is_approved_caterer = is_approved_caterer
        cls.commit_function()

    @classmethod
    def venue_get_caterer_for_event(cls, venue_id):
        """
        VenueGetCaterer query for getting list of event for caterer
        :param venue_id: from selected venue from caterer
        :return: VenueGetCaterer query by joining Caterer table
        """
        return cls.query.join(Caterer, cls.caterer_id == Caterer.id).filter(
            cls.caterer_id == Caterer.id).filter(cls.venue_id == venue_id).filter(
            cls.is_approved_caterer == True).all()

    @classmethod
    def caterer_query_for_event(cls, caterer_id):
        """
        list of events where caterer has decorated the venue
        :param caterer_id: from current user's id
        :return: VenueGetCaterer query by filtering caterer_id
        """
        return cls.query.filter_by(caterer_id=caterer_id).first()

    @classmethod
    def get_caterer_query_for_event(cls):
        """
        caterer get list of event where he has served the food
        :return: VenueGetCaterer query by joining Caterer table
        """
        return cls.query.join(Caterer, cls.caterer_id == Caterer.id).filter(
            cls.caterer_id == Caterer.id).all()
