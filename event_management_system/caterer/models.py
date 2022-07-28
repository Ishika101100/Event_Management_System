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
    def save_caterer(cls, user_id):
        """
        save user as caterer
        :param user_id: User table's id where user_type=4(caterer) is user_id of Caterer table
        :return:add user details in Caterer table
        """
        caterer = cls(user_id=user_id)
        db.session.add(caterer)
        db.session.commit()
        return caterer

    @classmethod
    def get_caterer_for_venue(cls, user_id):
        """
        query to get list of caterers
        :param user_id: from the list of caterer id's got in venue get caterer list
        :return:list of caterers query
        """
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_current_caterer(cls):
        """
        query to get id from caterer table by filtering current user's id from Users table
        :return:Get current user's caterer details
        """
        return cls.query.filter_by(user_id=current_user.id).first()


class FoodCategory(db.Model):
    """Add food category in the database"""
    __tablename__ = "food_category"
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String)
    caterer = db.relationship("CatererGetFoodCategory", backref='caterer_get_foodcategory', lazy=True)

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
    def get_food_category(cls, food_type):
        """
        caterer adds food category
        :param food_type: from the add food category form
        :return:food type in food category table
        """
        food_category_obj = cls(food_type=food_type)
        cls.add_function(food_category_obj)
        cls.commit_function()
        return food_category_obj

    @classmethod
    def food_category_query(cls, food_category_id):
        """
        getting food_category_id of category to update and delete food category
        :param food_category_id: from caterer's id
        :return: FoodCategory table by filtering food_category_id
        """
        return cls.query.filter_by(id=food_category_id).first()

    @classmethod
    def update_category(cls, food_category_id, food_category):
        """
        caterer updates it's added category type
        :param food_category_id: from selected category in the template
        :param food_category: from selected category in the template
        :return: save updated category type in database
        """
        category = FoodCategory.food_category_query(food_category_id=food_category_id)
        category.food_type = food_category
        cls.commit_function()

    @classmethod
    def delete_category(cls, food_category_id):
        """
        caterer deletes it's added category type
        :param food_category: from selected category in the template
        :return: delete category type in database
        """
        category = FoodCategory.food_category_query(food_category_id=food_category_id)
        cls.delete_function(category)
        cls.commit_function()


class CatererGetFoodCategory(db.Model):
    """Mapping table of caterer and food category"""
    __tablename__ = "caterer_get_food_category"
    __table_args__ = (
        PrimaryKeyConstraint('food_category_id', 'caterer_id'),
    )
    food_category_id = db.Column(db.Integer, db.ForeignKey('food_category.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
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
    def get_food_charges(cls, caterer_id, food_category_id, charges):
        """
        adding caterer it's food category and charges for that food category in CatererGetFoodCategory table.
        :param caterer_id: current user's id is same as caterer's user_id and from user_id we get caterer_id
        :param food_category_id:caterer add food category and then from then we get food_category_id
        :param charges:from add category form we get charges
        :return:adding caterer_id, food_category_id and charges in CatererGetFoodCategory table
        """
        food_charge_obj = cls(caterer_id=caterer_id, food_category_id=food_category_id,
                              charges=charges)
        cls.add_function(food_charge_obj)
        cls.commit_function()
        return food_charge_obj

    @classmethod
    def get_caterer_query(cls, caterer_id):
        """
        to view caterer its food categories and charges
        :param caterer_id: by getting current caterer id
        :return:CatererGetFoodCategory table by filtering caterer id
        """
        return cls.query.filter_by(caterer_id=caterer_id).all()

    @classmethod
    def charge_query_for_caterer(cls, caterer_id, food_category_id):
        """
        getting charge of category to update and delete food category
        :param caterer_id:from current user's id
        :param food_category_id: from caterer's id
        :return:CatererGetFoodCategory table by filtering caterer_id and food_category_id
        """
        return cls.query.filter_by(caterer_id=caterer_id,
                                   food_category_id=food_category_id).first()

    @classmethod
    def update_charge(cls, caterer_id, food_category_id, charges):
        """
        Caterer can update it's category's charges
        :param caterer_id: from current user's id
        :param food_category_id: from form of update details
        :param charges: from form of update details
        :return: save updated charges to the database
        """
        charge = cls.charge_query_for_caterer(caterer_id=caterer_id,
                                              food_category_id=food_category_id)
        charge.charges = charges
        cls.commit_function()

    @classmethod
    def delete_charge(cls, caterer_id, food_category_id):
        """
        Caterer can delete it's category's charges
        :param caterer_id: from current user's id
        :param food_category_id: from caterer's id
        :param charges: from caterer's id
        :return: delete charges to the database
        """
        charge = cls.charge_query_for_caterer(caterer_id=caterer_id,
                                              food_category_id=food_category_id)
        cls.delete_function(charge)
        cls.commit_function()

    @classmethod
    def get_caterer_food_cate_for_event(cls, caterer_id):
        """
        provide caterer details to user for booking event
        :param caterer_id: from ajax call on the basis of user's selected venue
        :return:CatererGetFoodCategory table by filtering caterer id
        """
        return cls.query.filter_by(caterer_id=caterer_id).all()
