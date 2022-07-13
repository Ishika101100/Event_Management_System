from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref

from event_management_system import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """add user in the database"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    venues = db.relationship("Venues", backref='venue_name', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    mobile_number = db.Column(db.String(12), nullable=False)
    address = db.Column(db.TEXT, nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    caterer = db.relationship("Caterer", backref='user_get_caterer', cascade="all, delete-orphan", lazy="joined")
    decorator = db.relationship("Decorator", backref='user_get_decorator', cascade="all, delete-orphan", lazy="joined")
    event = db.relationship("Event", backref='Event_get_user', cascade="all, delete-orphan", lazy="joined")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Event(db.Model):
    """add event in the database"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    no_of_guests = db.Column(db.Integer, nullable=False)
    is_approved_by_venue = db.Column(db.Boolean)
    decorator_charge = db.Column(db.Integer, default=0)
    caterer_charge = db.Column(db.Integer, nullable=False, default=0)
    venue_charge = db.Column(db.Integer, nullable=False, default=0)
    Total_charge = db.Column(db.Integer, nullable=True, default=0)


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


class Decorator(db.Model):
    """add decorator in the database"""
    __tablename__ = "decorator"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    decoration_type = db.relationship("DecoratorGetTypes", backref='decorator_get_types', lazy=True)
    venues = db.relationship("VenueGetDecorator", backref=backref("venue_get_decorators", uselist=False))
    # event = db.relationship("Event", backref="decorator_get_event", cascade="all, delete-orphan", lazy="joined")
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


class VenueGetDecorator(db.Model):
    """mapping table of venue and decorator"""
    __tablename__ = "venue_get_decorator"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'decorator_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    is_approved_decorator = db.Column(db.Boolean)


class Caterer(db.Model):
    """add caterer in the database"""
    __tablename__ = "caterer"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_category = db.relationship("CatererGetFoodCategory", backref='caterer_get_food_category', lazy=True)
    venues = db.relationship("VenueGetCaterer", backref='venue_get_caterer', lazy=True)
    event = db.relationship("Event", backref='caterer_get_event', cascade="all, delete-orphan", lazy="joined")
    user = db.relationship('User', backref=backref("User_for_caterer", uselist=False))

    def __repr__(self):
        return self.id


class FoodCategory(db.Model):
    """Add food category in the database"""
    __tablename__ = "food_category"
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String)
    caterer = db.relationship("CatererGetFoodCategory", backref='caterer_get_foodcategory', lazy=True)


class CatererGetFoodCategory(db.Model):
    """Mapping table of caterer and food category"""
    __tablename__ = "caterer_get_food_category"
    __table_args__ = (
        PrimaryKeyConstraint('food_category_id', 'caterer_id'),
    )
    food_category_id = db.Column(db.Integer, db.ForeignKey('food_category.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    charges = db.Column(db.Integer)


class VenueGetCaterer(db.Model):
    """mapping table of venue and caterer"""
    __tablename__ = "venue_get_caterer"
    __table_args__ = (
        PrimaryKeyConstraint('venue_id', 'caterer_id'),
    )

    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    is_approved_caterer = db.Column(db.Boolean)


class EventCategory(db.Model):
    """add event category in the database"""
    __tablename__ = "event_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return self.name


class UserType(db.Model):
    """add user type in the database"""
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship("User", backref='user_get_user_type', cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return self.user_type
