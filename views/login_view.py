import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

def login_view(self, values):
  self.response.out.write(template.render('views/login.html', values))