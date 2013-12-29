import webapp2

class TaskHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("HELLO")