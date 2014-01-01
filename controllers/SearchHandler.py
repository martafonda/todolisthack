# Libraries
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2

from models.Task import Task

class SearchHandler(webapp2.RequestHandler):
  def get(self):
    user_list = db.GqlQuery( 'SELECT * FROM User')
    current_user = users.get_current_user()
    word=self.request.get('search')
    task_list = db.GqlQuery('SELECT * FROM Task WHERE title = :1 ORDER BY date', word)
    values = {'task' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': task_list,
              'user': current_user}
    self.response.out.write(template.render('views/main.html', values))
  def post(self):
    user_list = db.GqlQuery( 'SELECT * FROM User')
    current_user = users.get_current_user()
    word=self.request.get('search')
    task_list = db.GqlQuery('SELECT * FROM Task WHERE title = :1 ORDER BY date', word)
    values = {'task' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': task_list,
              'user': current_user}
    self.response.out.write(template.render('views/main.html', values))
