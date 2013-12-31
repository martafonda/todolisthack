# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

from controllers.TaskHandler import TaskCrud

class DeleteTaskHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:

        self.redirect('/')
    else:
        self.redirect('/')

  def post(self):
    user = users.get_current_user()
    crud = TaskCrud(cid)
    if user:
        crud.delete_task(cid)
        values = { 'user': user }
        self.response.out.write(template.render('views/new_task.html', values))
    else:
        self.redirect('/')