from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from event_management_system import db
from event_management_system.book_event.forms import EventForm
from event_management_system.models import Venues, EventCategory, UserType

venue = [
    {
        'name': 'Venue 1',
        'address': 'Venue 1 Address',
        'contact_number': '9876543210',
        'email_id': 'venue1@gmail.com'
    },
    {
        'name': 'Venue 2',
        'address': 'Venue 2 Address',
        'contact_number': '9876543210',
        'email_id': 'venue2@gmail.com'
    }
]
book_event = Blueprint('book_event', __name__)


@book_event.route("/venue", methods=['GET'])
def venue_add():
    for i in venue:
        book = Venues(
            name=i.get("name"),
            address=i.get("address"),
            contact_number=i.get("contact_number"),
            email_address=i.get("email_id")
        )
        db.session.add(book)
        db.session.commit()
    # print("venue-------->", venue)
    return render_template('book_event.html')


event_category = [
    {
        'name': 'Social Events',
    },
    {
        'name': 'Corporate events',
    }
]

@book_event.route("/event_category", methods=['GET'])
def event_category_add():
    form=EventForm()
    for i in event_category:
        event = EventCategory(
            name=i.get("name")
        )
        db.session.add(event)
        db.session.commit()
    return render_template('book_event.html',form=form)


@book_event.route("/book_event")
@login_required
def category():
    if current_user.user_type == 1:
        form = EventForm()
        cate = EventCategory.query.all()
        venue_get=Venues.query.all()
        return render_template('book_event.html', cate=cate,venue_get=venue_get,form=form)
    else:
        flash("Only users can access this page")
        return redirect(url_for('main.home'))



