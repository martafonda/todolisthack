import webapp2
from google.appengine.api import users

class TaskHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    user = users.get_current_user()
    self.response.out.write('Hello, ' + user.nickname())
    self.response.out.write("HELLO THERE")