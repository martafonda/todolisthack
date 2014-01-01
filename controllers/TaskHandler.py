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
    user_email = current_user.email()
    user_tasks = db.GqlQuery( "SELECT * FROM Task WHERE author = :1 ORDER BY date", user_email)
    values = {'users' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': user_tasks,
              'user': current_user}
    self.response.out.write(template.render('views/main.html', values))
  
  def post(self):
    task = Task(author=self.request.get('author'),
                title=self.request.get('title'),
                description = self.request.get('description'))
    task.put()
    self.redirect('/')
class TaskCrud(webapp2.RequestHandler):
  def __init__(self, cid):
        self.cid = cid

  def show_task(self):
        return db.GqlQuery('SELECT * FROM Task WHERE tid = :1',
                           self.cid).get()

  def update_task(self, author, description):

        task = db.GqlQuery('SELECT * FROM Task WHERE tid = :1',
                              self.cid).get()
        if not task:
            new_task = Task(tid=self.cid,
                            author=author,
                            title=title,
                            description=description)
            new_task.put()
        else:
            setattr(task, "author", author)
            setattr(task, "title", title)
            setattr(task, "description", description)
            task.put()
        return("OK")

  def delete_task(self):
        task = db.GqlQuery('SELECT * FROM Task WHERE tid = :1',
                              self.cid).get()
        db.delete(task)
