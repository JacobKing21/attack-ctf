from functools import wraps
from flask import Flask, render_template
from flask_login import UserMixin, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ctf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'users.login'


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorised notice!
                return render_template('403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


class users(db.Model, UserMixin):
    __tablename__ = 'users'

    # User information
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False, default='user')

    # User auth information
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    flag_recon = db.Column(db.Integer, nullable=False, default=0)

    # User constructor
    def __init__(self, role, email, password, flag_recon):
        self.role = role
        self.email = email
        # Generating password hash
        self.password = generate_password_hash(password)
        self.flag_recon = flag_recon


class products(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


def init_db():
    db.drop_all()
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """Getting the user id from login manager to determine which user is logged in"""
    return users.query.get(int(user_id))


from admin.views import admin_blueprint
from users.views import users_blueprint
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
