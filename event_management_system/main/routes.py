from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


# @main.route("/book_event")
# @login_required
# def book_event():
#     return render_template('book_event.html', title='Book Event')

@main.route("/get_bill")
@login_required
def get_bill():
    if current_user.user_type == 1:
        return render_template('get_bill.html')
    else:
        flash("Only users can access this page")
        return redirect(url_for('main.home'))


@main.route("/contact")
@login_required
def contact():
    return render_template('contact.html', title='Contact Us')