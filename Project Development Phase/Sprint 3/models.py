import datetime
from app import db, bcrypt
#from project import database as db

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)    
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    home_applied = db.Column(db.Boolean, nullable=False, default=False)
    business_applied = db.Column(db.Boolean, nullable=False, default=False)
    home_status = db.Column(db.String, nullable=True)    
    business_status = db.Column(db.String, nullable=True)    
    
    
    def __init__(self, name, email, password, confirmed, confirmed_on=None, home_applied =None, business_applied=None, home_status=None, business_status=None ):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.home_applied = home_applied
        self.business_applied = business_applied
        self.home_status = home_status
        self.business_status = business_status

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id