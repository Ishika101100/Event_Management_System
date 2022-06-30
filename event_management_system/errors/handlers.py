from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """If user tries to access the page that doesn't exist then 404 error page will be shown"""
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """If current user doesn't have access to a particular page and still user tries to access that page then 403
    error page will be shown """

    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """If there is any server error then error 500 page will be shown"""
    return render_template('errors/500.html'), 500
