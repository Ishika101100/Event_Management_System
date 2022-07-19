from flask_login import current_user
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import backref

from event_management_system import db


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

def save_caterer(user_id):
    caterer = Caterer(user_id=user_id)
    db.session.add(caterer)
    db.session.commit()
    return caterer

def get_caterer_for_venue(user_id):
    return Caterer.query.filter_by(user_id=user_id).first()

def get_current_caterer():
    return Caterer.query.filter_by(user_id=current_user.id).first()

def get_food_category(food_type):
    return FoodCategory(food_type=food_type)

def get_food_charges(caterer_id,food_category_id,charges):
    return CatererGetFoodCategory(caterer_id=caterer_id, food_category_id=food_category_id,
                           charges=charges)

def get_caterer_query(caterer_id):
    return CatererGetFoodCategory.query.filter_by(caterer_id=caterer_id).all()

def charge_query_for_caterer(caterer_id,food_category_id):
    return CatererGetFoodCategory.query.filter_by(caterer_id=caterer_id,
                                                    food_category_id=food_category_id).first()

def food_category_query(food_category_id):
    return FoodCategory.query.filter_by(id=food_category_id).first()