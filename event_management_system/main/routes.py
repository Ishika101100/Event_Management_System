from flask import render_template, request, Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/book_event")
@login_required
def book_event():
    return render_template('book_event.html', title='Book Event')


@main.route("/get_bill")
@login_required
def get_bill():
    return render_template('get_bill.html', title='Get Bill')


@main.route("/contact")
@login_required
def contact():
    return render_template('contact.html', title='Contact Us')