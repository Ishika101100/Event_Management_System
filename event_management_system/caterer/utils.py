from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def is_caterer(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.user_type == 4:
            return f()
        flash("Only caterer can access this page", "warning")
        return redirect(url_for('main.home'))

    return wrapped