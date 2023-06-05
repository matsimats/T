from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'moj-sekret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from views import *

from flask_migrate import Migrate

migrate = Migrate(app, db)
#init służy tylko za inicjowania
#flask db init
#flask db migrate -m "Added new column to User model"
#flask db upgrade


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
