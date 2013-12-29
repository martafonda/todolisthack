# Libraries
import webapp2

class ProfileHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("WE ARE IN PROFILE")