from . import db
from datetime import datetime


class website: # use the keyword class

    def __init__(self, name1, email1): #constuct an object of this class
        self.name = name1 # define and access attributes of the class using self.
        self.email = email1
        self.type='normal'
        self.password_hash=None
        self.comment = list()

     #  the set password method goes here
    def set_password(self, password):
        self.password_hash=password

    def __repr__(self):
        s="Name: {}, Email: {}, Type: {}, Password {}"
        s= s.format(self.name, self.email, self.type, self.password_hash)
        return s

    def set_comments(self,comment):
        str = 'Name {0}'
        str.format(self.name)
        return str

#class Admin(User): # derived class of User1
#    def __init__(self, name, email, privilege):
#        super().__init__(name,email) #when you call base class method super()
#        self.type='admin'
#        self.privilege=privilege

class Cuisine(db.Model):
    __tablename__ = 'tbl_cuisine'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80))
    description = db.Column(db.String(200))
    date_from   = db.Column(db.DateTime)
    date_to     = db.Column(db.DateTime)
    image       = db.Column(db.String(400))
    quantity    = db.Column(db.Integer())
    price       = db.Column(db.Integer())
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    # comments = db.relationship('Comment', backref='Cuisine')
 
    def __repr__(self): 
        return "<Name: {}>".format(self.name)
        
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    website_id = db.Column(db.Interger, db.ForeignKey('website.id'))

#    def __repr__(self):
#        return "<Comment: {}>".format(self.text)
   # def __init__(self, user, text, created_at):
    #    self.user = user
     #   self.text = text
      #  self.create_at = created_at

    #def __repr__(self):
     #   str = 'User {0}, \n Text {1}'
      #  str.format(self.user, self.text)
       # return str



#create a base class
user = User('countvoncount', 'cvc@sstreet.com')
user.set_password('vatesdenoovdeday')

# create the derived or admin class
user = User('kermit', 'kermie@x.sstreet.com', 'xyzere')

 # the base class method is accessible in the derived class
user.set_password('dreamersandme') 

#print both the classes
print(user)
