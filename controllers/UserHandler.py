#Libraries
import webapp2
from google.appengine.api import users
from google.appengine.ext import db

from models.User import User

class UserHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("HELLO")

class UserCrud(webapp2.RequestHandler):
  def __init__(self, cid):
        self.cid = cid

  def show_user(self):
        return db.GqlQuery('SELECT * FROM User WHERE uid = :1',
                           self.cid).get()

  def update_user(self, first_name, last_name, email):
        #  Validate the input
        if first_name == None or "":
            return("first_name")
        elif last_name == None or "":
            return("last_name")

        user = db.GqlQuery('SELECT * FROM User WHERE uid = :1',
                              self.cid).get()
        if not user:
            new_user = User(uid=self.cid,
                              first_name=first_name,
                              last_name=last_name,
                              email=email,
                              validated=False)
            new_user.put()
        else:
            setattr(user, "first_name", first_name)
            setattr(user, "last_name", last_name)
            setattr(user, "email", email)
            user.put()
        return("OK")

  def delete_user(self):
        user = db.GqlQuery('SELECT * FROM User WHERE uid = :1',
                              self.cid).get()
        db.delete(user)