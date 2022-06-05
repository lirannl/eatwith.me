from hashlib import sha256
from random import Random, random
from . import db
from datetime import datetime
import uuid


class website:  # use the keyword class

    def __init__(self, name1, email1):  # constuct an object of this class
        # define and access attributes of the class using self.
        self.name = name1
        self.email = email1
        self.type = 'normal'
        self.password_hash = None
        self.comment = list()

     #  the set password method goes here
    def set_password(self, password):
        self.password_hash = password

    def __repr__(self):
        s = "Name: {}, Email: {}, Type: {}, Password {}"
        s = s.format(self.name, self.email, self.type, self.password_hash)
        return s

    def set_comments(self, comment):
        str = 'Name {0}'
        str.format(self.name)
        return str


class User:
    __tablename__ = "User"
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), unique=True)
    password_hash: str = db.Column(db.String(128))
    contact_number: str = db.Column(db.String(64), unique=True)
    password_salt: bytes = db.Column(db.BLOB(64))

    def __init__(self, username: str):
        self.username = username
        self.type = 'normal'

    def set_password(self, password: str):
        self.password_salt = Random().randbytes(64)
        self.password_hash = sha256(
            self.password_salt + password.encode()).hexdigest()

    def verify_password(self, password: str):
        return sha256(self.password_salt + password.encode())\
            .hexdigest() == self.password_hash

    def __repr__(self):
        s = "Name: {0}, type: {1}\n"\
            .format(self.username, self.type)
        return s

class Admin(User):  # derived class of User1
    def __init__(self, username, privilege):
        super().__init__(username)  # when you call base class method super()
        self.type = 'admin'
        self.privilege = privilege


class Cuisine():
    __tablename__ = "Cuisine"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True)

    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self.name = name


class Event():
    __tablename__ = "Event"
    id: int = db.Column(db.Integer, primary_key=True)
    cuisineId: int = db.Column(db.Integer, db.ForeignKey('Cuisine.id'))
    cuisine: Cuisine = property(lambda self: Cuisine.query.get(self.cuisineId))
    hostId: int = db.Column(db.Integer, db.ForeignKey('User.id'))
    host: User = property(lambda self: User.query.get(self.hostId))
    ticketPrice: int = db.Column(db.Integer)
    address: str = db.Column(db.String(256))
    coarseLocation: str = db.Column(db.String(64))
    capacity: int = db.Column(db.Integer)
    startTime: datetime = db.Column(db.DateTime)
    isActive: bool = db.Column(db.Boolean)
    attributes: property(lambda self: db.session.query('EventAttribute').filter(lambda attr: attr.eventId == self.id))

    def __init__(self, cuisine: Cuisine, host: User, ticketPrice: int, address: str, coarseLocation: str,
                 capacity: int, startTime: datetime):
        self.cuisineId = cuisine.id
        self.hostId = host.id
        self.ticketPrice = ticketPrice
        self.address = address
        self.coarseLocation = coarseLocation
        self.capacity = capacity
        self.startTime = startTime
        self.isActive = True

class Attribute():
    __tablename__ = "Attribute"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True)

    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self.name = name

# class Comment(db.Model):
#    __tablename__ = 'comments'
#    id = db.Column(db.Integer, primary_key=True)
#    text = db.Column(db.DateTime, default=datetime.now())
#    #add the foreign keys
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#    website_id = db.Column(db.Interger, db.ForeignKey('website.id'))

#    def __repr__(self):
#        return "<Comment: {}>".format(self.text)
   # def __init__(self, user, text, created_at):
    #    self.user = user
    #   self.text = text
    #  self.create_at = created_at

    # def __repr__(self):
    #   str = 'User {0}, \n Text {1}'
    #  str.format(self.user, self.text)
    # return str

# create a base class
normal_user = User('cvc@sstreet.com')
normal_user.set_password('vatesdenoovdeday')

# create the derived or admin class
admin_user = Admin('kermie@x.sstreet.com', 'xyzere')

# the base class method is accessible in the derived class
admin_user.set_password('dreamersandme')

# print both the classes
print(normal_user)
print(admin_user)


# create instance of the Hotel class: __init__ method is called here
#hotel_in_brisbane = Hotel('brisbane', 'Description of Brisbane')
# print(hotel_in_brisbane)

# create instance of the class
#hotel_in_sydney = Hotel('sydney', 'Close to Opera house')
#hotel_in_sydney.add_room('standard','basic room', 45,200)
# print(hotel_in_sydney)
#
#hotel_in_brisbane.add_room('standard',' basic room in Brisbane', 30, 120)
# print(hotel_in_brisbane)

# you could create independent room objects but current signature of hotel
# does not let you pass the child object, it takes control of the child object
#std_room1 = Room('standard', 'Basic room', 30,110)
#std_room2 = Room('standard', 'Basic room', 45,200)
