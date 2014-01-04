#!/usr/bin/env python
# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

# Controllers
from controllers.TaskHandler import TaskCrud

class DeleteTaskHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/')

  def post(self):
    user = users.get_current_user()
    cid  = self.request.get('id')
    crud = TaskCrud(cid)
    if user:
        crud.delete_task()
    else:
        self.redirect('/')