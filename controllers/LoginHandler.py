# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    values = {'login_url': users.create_login_url("/profile")}
    self.response.out.write(template.render('views/login.html', values))