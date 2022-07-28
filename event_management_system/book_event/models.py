from datetime import date

from flask_login import current_user

from event_management_system import db


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
    def get_event_detail_for_venue(cls, venue_id, is_approved_by_venue):
        """query to provide event details with venue approval status to venue"""
        return cls.query.filter_by(venue_id=venue_id).filter_by(is_approved_by_venue=is_approved_by_venue).all()

    @classmethod
    def get_event_details_for_decorator(cls, decorator_id):
        """query to provide event details to decorator"""
        return cls.query.filter_by(decorator_id=decorator_id).all()

    @classmethod
    def event_detail_for_caterer(cls, caterer_id):
        """query to provide event details to caterer"""
        return cls.query.filter_by(caterer_id=caterer_id).all()

    @classmethod
    def get_event_query(cls, event_id):
        """query to provide event details to venue for checking event booking request"""
        return cls.query.filter_by(id=event_id).first()

    @classmethod
    def update_booking_request(cls, event_id, check_venue_approval):
        """
        updating booking request made my user
        :param event_id: from current user's id
        :param check_venue_approval:from event id
        :return:save event object with approval_status
        """
        event_obj = Event.get_event_query(event_id)
        event_obj.is_approved_by_venue = check_venue_approval
        cls.commit_function()

    @classmethod
    def get_event(cls, venue_id):
        """query to check if user's any event at same day and same venue exists or not"""
        return cls.query.filter_by(user_id=current_user.id).filter_by(
            venue_id=venue_id).filter(cls.date >= date.today()).first()

    @classmethod
    def book_event_for_category_one(cls, title, category, date, venue_id, decorator_id, caterer_id, start_time,
                                    end_time,
                                    no_of_guests, venue_charge, decorator_charge, caterer_charge, Total_charge):
        """query to book event if event category is social event"""
        book_event_obj = cls(user_id=current_user.id, title=title,
                             category=category, date=date,
                             venue_id=venue_id,
                             decorator_id=decorator_id,
                             caterer_id=caterer_id,
                             start_time=start_time,
                             end_time=end_time, no_of_guests=no_of_guests,
                             venue_charge=venue_charge,
                             decorator_charge=decorator_charge,
                             caterer_charge=caterer_charge,
                             Total_charge=Total_charge)
        cls.add_function(book_event_obj)
        cls.commit_function()

    @classmethod
    def book_event_for_category_two(cls, title, category, date, venue_id, caterer_id, start_time, end_time,
                                    no_of_guests,
                                    venue_charge, caterer_charge, Total_charge):
        """query to book event if event category is corporate event"""
        book_event_obj = cls(user_id=current_user.id, title=title,
                             category=category, date=date,
                             venue_id=venue_id,
                             caterer_id=caterer_id,
                             start_time=start_time,
                             end_time=end_time, no_of_guests=no_of_guests,
                             venue_charge=venue_charge,
                             caterer_charge=caterer_charge,
                             Total_charge=Total_charge)
        cls.add_function(book_event_obj)
        cls.commit_function()

    @classmethod
    def get_current_event(cls):
        """query to get all events of the current user"""
        return cls.query.filter_by(user_id=current_user.id).all()

    @classmethod
    def update_event_data(cls, event_id, title, no_of_guests, date, start_time, end_time):
        """
        saving updated event details into the database
        :param event_id: from current user's id
        :param title:from user's data value in form
        :param no_of_guests:from user's data value in form
        :param date:from user's data value in form
        :param start_time:from user's data value in form
        :param end_time:from user's data value in form
        :return:save updated values in database
        """
        event_obj = cls.get_event_query(event_id)
        event_obj.title = title
        event_obj.no_of_guests = no_of_guests
        event_obj.date = date
        event_obj.start_time = start_time
        event_obj.end_time = end_time
        cls.commit_function()

    @classmethod
    def delete_event_data(cls, event_id):
        """
        delete user's event
        :param event_id: from current user's id
        :return: deleting event from the database
        """
        event_obj = cls.get_event_query(event_id)
        cls.delete_function(event_obj)
        cls.commit_function()


class EventCategory(db.Model):
    """add event category in the database"""
    __tablename__ = "event_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

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
        return self.name

    @staticmethod
    def get_event_category():
        """get event category"""
        return EventCategory.query.all()
