# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

from controllers.TaskHandler import TaskCrud

from models.Task import Task


class NewTaskHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
        values = { 'user': user }
        self.response.out.write(template.render('views/new_task.html', values))
    else:
        self.redirect('/')

  def post(self):
    task = Task(author=self.request.get('author'),
                content = self.request.get('content'))
    task.put()
    self.redirect('/')