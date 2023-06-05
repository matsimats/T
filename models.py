from app import db  # Zaimportuj db z app.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tutaj idzie reszta twojego kodu...


from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    can_add = db.Column(db.Boolean, default=True)
    can_edit = db.Column(db.Boolean, default=True)
    can_delete = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scenario = db.Column(db.Text, nullable=False)
    suite = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='not_set') # new field
    date_added = db.Column(db.String, default=datetime.utcnow)
    last_modified = db.Column(db.String, default=datetime.utcnow, onupdate=datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # relationships
    user = db.relationship('User', backref='test_cases')



