from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """returns home page"""
    return render_template('home.html')


@main.route("/about")
def about():
    """returns about page"""
    return render_template('about.html', title='About')


@main.route("/get_bill")
@login_required
def get_bill():
    """If current user type is 1(User) then only user can access this page"""
    if current_user.user_type == 1:
        return render_template('get_bill.html')
    else:
        flash("Only users can access this page")
        return redirect(url_for('main.home'))
