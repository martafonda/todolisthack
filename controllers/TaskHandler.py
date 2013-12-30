# Libraries
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2

from models.Task import Task

class TaskHandler(webapp2.RequestHandler):
  def get(self):
    user_list = db.GqlQuery( 'SELECT * FROM User')
    current_user = users.get_current_user()
    user_tasks = db.GqlQuery( 'SELECT * FROM Task ORDER BY date' )
    values = {'users' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': user_tasks,
              'current': current_user}
    self.response.out.write(template.render('views/main.html', values))
  
  def post(self):
    task = Task(content = self.request.get('content'))
    task.put()
