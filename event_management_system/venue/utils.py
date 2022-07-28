from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from event_management_system.venue.constants import IF_NOT_VENUE_MESSAGE


def is_venue(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.user_type == 2:
            return f()
        flash(IF_NOT_VENUE_MESSAGE, "warning")
        return redirect(url_for('main.home'))

    return wrapped
