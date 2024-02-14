from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets
from sqlalchemy.dialects.postgresql import UUID

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, first_name='', last_name='', password='', email='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'<User | collector_id: {self.id} | email: {self.email}>'

class Car(db.Model):
    __tablename__ = 'car'
    car_id = db.Column(db.String(100), primary_key = True, default=uuid.uuid4)
    year = db.Column(db.String, nullable = False)
    color = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    collector_id = db.Column(db.String, db.ForeignKey(User.id), nullable = False) 

    def __init__(self,year,color,make,model,user_token, collector_id=User.id,id = ''):
        self.id = self.set_id()
        self.year = year
        self.color = color
        self.make = make
        self.model = model
        self.user_token = user_token

    def __repr__(self):
        return f'<Car | id: {self.id} | year: {self.year} | color | {self.collector_id} | make: {self.make} | model | {self.model}>'

    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'year','color','make', 'model']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)