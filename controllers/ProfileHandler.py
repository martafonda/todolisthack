# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import db
#Models
from models.User import User

#Main Profile Handler
class ProfileHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    email = user.email()
    qry = db.GqlQuery("SELECT * FROM User WHERE email = :1", email)
    user_db = qry.get()
    
    if user_db is None:
        values = {'user': user}
        self.response.out.write(template.render('views/profile.html', values))
    else:
        self.redirect('/')

  def post(self):
        user = users.get_current_user()
        uid = user.user_id()
        crud = UserCrud(uid)

        #CRUD usage to save modifications in Users. If user doesn't exist the CRUD
        #method "update_user" creates new one
        qry = crud.update_user(first_name=self.request.get('first_name'),
                            last_name=self.request.get('last_name'),
                            email=self.request.get('email'))
        if qry != "OK":
            self.abort(500)
        #Email sender
        mail.send_mail(sender="Example.com Support <martafondapascual@gmail.com>",
              to= self.request.get('email'),
              subject="Your account has been approved",
              body="""
                Welcome to TODOListHack

                Thank you and enjoy your tasks

                The todolisthack.com Team
                """)

        self.redirect('/')

class UserCrud(webapp2.RequestHandler):
  def __init__(self, cid):
        self.cid = cid

  def show_user(self):
        return db.GqlQuery('SELECT * FROM User WHERE uid = :1',
                           self.cid).get()

  def update_user(self, first_name, last_name, email):

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
