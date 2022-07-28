from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """Created app and registered blueprint"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from event_management_system.users.routes import users
    from event_management_system.errors.handlers import errors
    from event_management_system.book_event.routes import book_event
    from event_management_system.venue.routes import venue
    from event_management_system.decorator.routes import decorator
    from event_management_system.caterer.routes import caterer

    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(book_event)
    app.register_blueprint(venue)
    app.register_blueprint(decorator)
    app.register_blueprint(caterer)

    return app
