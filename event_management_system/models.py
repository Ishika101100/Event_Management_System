from event_management_system import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    mobile_number = db.Column(db.String(12), nullable=False)
    address = db.Column(db.TEXT, nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# class Event(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     title = db.column()
#     category = db.column()
#     date = db.column()
#     venue_id = db.column()
#     time = db.column()
#     duration = db.column()
#     no_of_guests = db.column()
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Venues(db.Model):

    __tablename__ = "venues"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    decorator_id = db.Column(db.Integer, db.ForeignKey('decorator.id'))
    caterer_id = db.Column(db.Integer, db.ForeignKey('caterer.id'))
    venue_type = db.Column(db.String)
    capacity = db.Column(db.Integer)
    charges = db.Column(db.Integer)

    def __repr__(self):
        return self.id


class Caterer(db.Model):
    __tablename__ = "caterer"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_category_id = db.Column(db.Integer, db.ForeignKey('food_category.id'))
    charges = db.Column(db.Integer)

    def __repr__(self):
        return self.id


class FoodCategory(db.Model):
    __tablename__ = "food_category"
    id = db.Column(db.Integer, primary_key=True)
    food_type = db.Column(db.String)


class Decorator(db.Model):
    __tablename__ = "decorator"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    decoration_type_id = db.Column(db.Integer, db.ForeignKey('decorator_type.id'))
    charges = db.Column(db.Integer)

    def __repr__(self):
        return self.id


class DecorationType(db.Model):
    __tablename__ = "decorator_type"
    id = db.Column(db.Integer, primary_key=True)
    decoration_type = db.Column(db.String)


class EventCategory(db.Model):
    __tablename__ = "event_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return self.name


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return self.user_type
