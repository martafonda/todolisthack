# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

from controllers.TaskHandler import TaskCrud


class NewTaskHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
        values = {}
        self.response.out.write(template.render('views/new_task.html', values))
    else:
        self.redirect('/')

  def post(self):
    user = users.get_current_user()
    uid = user.user_id()
    crud = TaskCrud(uid)

    is_valid = crud.update_task(author=self.request.get(user.email),
                                content=self.request.get('content'))
    self.redirect('/')