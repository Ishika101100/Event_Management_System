from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from event_management_system.caterer.constants import CATERER_USER


def is_caterer(f):
    """
    checks if current user is caterer or not
    :param f: if user type is 4 then current use is caterer
    :return: url for home page
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.user_type == 4:
            return f()
        flash(CATERER_USER, "warning")
        return redirect(url_for('main.home'))

    return wrapped
