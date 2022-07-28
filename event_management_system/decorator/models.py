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
    def save_decorator(cls, user_id):
        """
        save current user as decorator
        :param user_id: id of current user is user_id for decorator
        :return: decorator table entry
        """
        decorator = cls(user_id=user_id)
        db.session.add(decorator)
        db.session.commit()
        return decorator

    @classmethod
    def get_decorator_for_venue(cls, user_id):
        """
        get decorator from user id
        :param user_id: from current user's id
        :return: Decorator table query filtered by user_id
        """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_current_decorator(cls):
        """
        get current decorator
        :return:
        """
        return cls.query.filter_by(user_id=current_user.id).first()


class DecoratorType(db.Model):
    """add decoration type in the database"""
    __tablename__ = "decorator_type"
    id = db.Column(db.Integer, primary_key=True)
    decoration_type = db.Column(db.String)
    decorator = db.relationship("DecoratorGetTypes", backref='decorator_get_decorationType', lazy=True)

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

    def __repr__(self):
        return self.id

    @classmethod
    def get_decor_category(cls, decoration_type):
        """
        decorator can add decoration category
        :param decoration_type: from decorator_id
        :return: DecoratorType table filtered by decoration_type
        """
        decor_category_obj = cls(decoration_type=decoration_type)
        cls.add_function(decor_category_obj)
        cls.commit_function()
        return decor_category_obj

    @classmethod
    def get_decoration_category(cls, decorator_type_id):
        """
        provide decorator decorator_type_id to update/delete decoration category
        :param decorator_type_id:from decorator id
        :return:DecoratorType table filtered by decorator_type_id
        """
        return cls.query.filter_by(id=decorator_type_id).first()

    @classmethod
    def update_decor_type(cls, decorator_type_id, decor_type):
        """
        decorator can update it's decorations types
        :param decorator_type_id: from selected decoration type in the website
        :param decor_type: from decorator_type_id
        :return: save updated changes to database
        """
        category = DecoratorType.get_decoration_category(decorator_type_id=decorator_type_id)
        category.decoration_type = decor_type
        cls.commit_function()

    @classmethod
    def delete_decor_type(cls, decorator_type_id):
        """
        decorator can delete it's decorations types
        :param decorator_type_id: from selected decoration type in the website
        :param decor_type: from decorator_type_id
        :return: save deleted changes to database
        """
        category = DecoratorType.get_decoration_category(decorator_type_id=decorator_type_id)
        cls.delete_function(category)
        cls.commit_function()


class DecoratorGetTypes(db.Model):
    """mapping table of decorator and decoration types"""
    __tablename__ = "decorator_get_types"
    __table_args__ = (
        PrimaryKeyConstraint('decorator_id', 'decoration_type_id'),
    )
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    decoration_type_id = db.Column(db.Integer, db.ForeignKey('decorator_type.id'))
    charges = db.Column(db.Integer)

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
    def decor_get_types(cls, decorator_id, decoration_type_id, charges):
        """
        adding decorator and decoration type details to DecoratorGetTypes table
        :param decorator_id: from current user's id
        :param decoration_type_id: from decorator id
        :param charges: from add category form
        :return: adding details to DecoratorGetTypes table
        """
        decor_type_obj = cls(decorator_id=decorator_id, decoration_type_id=decoration_type_id,
                             charges=charges)
        cls.add_function(decor_type_obj)
        cls.commit_function()

    @classmethod
    def get_decor_charges(cls, decorator_id, decoration_type_id):
        """
        decorator can update and delete its decoration charges
        :param decorator_id: from current user's id
        :param decoration_type_id:from decorator id
        :return:DecoratorGetTypes table filtered by decoration_id and decoration_type_id
        """
        return cls.query.filter_by(decorator_id=decorator_id,
                                   decoration_type_id=decoration_type_id).first()

    @classmethod
    def update_charges(cls, decorator_id, decorator_type_id, decor_charge):
        """
        decorator can update charges of a particular decoration type
        :param decorator_id: from current user's id
        :param decorator_type_id: from selected decoration type from the database
        :param decor_charge: from selected decoration type from the database
        :return: save updated charges to the database
        """
        charge = cls.get_decor_charges(decorator_id=decorator_id, decoration_type_id=decorator_type_id)
        charge.charges = decor_charge
        cls.commit_function()
        return charge

    @classmethod
    def delete_decor_charge(cls, decorator_id, decorator_type_id):
        """
        decorator can update charges of a particular decoration type
        :param decorator_id: from current user's id
        :param decorator_type_id: from selected decoration type from the database
        :return: save deleted charges to the database
        """
        charge = DecoratorGetTypes.get_decor_charges(decorator_id=decorator_id, decoration_type_id=decorator_type_id)
        cls.delete_function(charge)
        cls.commit_function()

    @classmethod
    def get_decorator_type(cls, decorator_id):
        """
        decorator can view his decoration category
        :param decorator_id: from current user's id
        :return:DecoratorGetTypes table filtered by decorator id
        """
        return cls.query.filter_by(decorator_id=decorator_id).all()

    @classmethod
    def get_decor_types_for_event(cls, decorator_id):
        """
        user can get list of decorator of his/her selected venue
        :param decorator_id: from selected venue id
        :return: DecoratorGetTypes table filtered by decorator id
        """
        return cls.query.filter_by(decorator_id=decorator_id).all()
