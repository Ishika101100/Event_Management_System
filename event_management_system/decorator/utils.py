from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from event_management_system.decorator.constants import USER_DECORATOR_MESSAGE


def is_decorator(f):
    """
    check if current user is decorator or not
    :param f: user_type == 3
    :return: redirect to home page
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.user_type == 3:
            return f()
        flash(USER_DECORATOR_MESSAGE, "warning")
        return redirect(url_for('main.home'))

    return wrapped
