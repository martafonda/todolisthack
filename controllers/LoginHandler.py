# Libraries
import webapp2
from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    values = {'login_url': users.create_login_url("/profile")}
    self.response.out.write(template.render('templates/login.html', values))