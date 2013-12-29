#Libraries
import webapp2
from google.appengine.api import users
#Views
from views.login_view import login_view

class UserHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("HELLO")

#CRUD
class CreateUser(webapp2.RequestHandler):
  def post(self):
    user = User(first_name = self.request.get('first_name'),
    last_name = self.request.get('last_name'),
    email = self.request.get('first_name'),
    validated = self.request.get('first_name'))

class ShowUser(webapp2.RequestHandler):

class EditUser(webapp2.RequestHandler):

class DestroyUser(webapp2.RequestHandler):

