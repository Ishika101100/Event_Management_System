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


class EventCategory(db.Model):
    """add event category in the database"""
    __tablename__ = "event_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return self.name


def get_event_detail_for_venue(venue_id, is_approved_by_venue):
    return Event.query.filter_by(venue_id=venue_id).filter_by(is_approved_by_venue=is_approved_by_venue).all()


def get_event_details_for_decorator(decorator_id):
    return Event.query.filter_by(decorator_id=decorator_id).all()


def get_event_obj_for_venue(event_id):
    return Event.query.filter_by(id=event_id).first()


def event_detail_for_caterer(caterer_id):
    return Event.query.filter_by(caterer_id=caterer_id).all()


def get_event_query(event_id):
    return Event.query.filter_by(id=event_id).first()


def get_event_category():
    return EventCategory.query.all()


def get_event(venue_id):
    return Event.query.filter_by(user_id=current_user.id).filter_by(
        venue_id=venue_id).filter(Event.date >= date.today()).first()


def book_event_for_category_one(title, category, date, venue_id, decorator_id, caterer_id, start_time, end_time,
                                no_of_guests, venue_charge, decorator_charge, caterer_charge, Total_charge):
    return Event(user_id=current_user.id, title=title,
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


def book_event_for_category_two(title, category, date, venue_id, caterer_id, start_time, end_time, no_of_guests,
                                venue_charge, caterer_charge, Total_charge):
    return Event(user_id=current_user.id, title=title,
                 category=category, date=date,
                 venue_id=venue_id,
                 caterer_id=caterer_id,
                 start_time=start_time,
                 end_time=end_time, no_of_guests=no_of_guests,
                 venue_charge=venue_charge,
                 caterer_charge=caterer_charge,
                 Total_charge=Total_charge)


def get_current_event():
    return Event.query.filter_by(user_id=current_user.id).all()
