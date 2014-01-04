# Libraries
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
import webapp2
import datetime

from models.Task import Task

class TaskHandler(webapp2.RequestHandler):
  def get(self):
    user_list = self.get_users()
    current_user = users.get_current_user()
    user_email = current_user.email()
    user_tasks = db.GqlQuery( "SELECT * FROM Task WHERE author = :1 ORDER BY date", user_email)
    values = {'users' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': user_tasks,
              'user': current_user}
    self.response.out.write(template.render('views/main.html', values))
  
  def get_users(self):
    users = memcache.get("users")
    if users is not None:
      return users
    else:
      users = self.retrieve_users()
      if not memcache.add("users", users, 10):
          logging.error("Memcache set failed.")
      return users
  
  def retrieve_users(self):
    return db.GqlQuery( 'SELECT * FROM User')

  def post(self):
    tid = self.request.get('id')
    crud = TaskCrud(tid)
    date = self.request.get('date')
    date_parsed = datetime.datetime.strptime(date, '%m/%d/%Y').date()
    if tid:
      qry = crud.update_task(author=self.request.get('author'),
                title=self.request.get('title'),
                description = self.request.get('description'),
                dones = self.request.get('done'),
                date = date_parsed)
    else:
      qry = crud.new_task(author=self.request.get('author'),
                title=self.request.get('title'),
                description = self.request.get('description'),
                date = date_parsed)
    self.response.out.write(template.render('views/new_task.html',qry))

class TaskCrud(webapp2.RequestHandler):
  def __init__(self, cid):
        self.cid = cid

  def show_task(self):
        return db.GqlQuery('SELECT * FROM Task WHERE tid= :1',
                           self.cid).get()
  def new_task(self,author, title, description,date):
        new_task = Task(__key__=self.cid,
                        author=author,
                        title=title,
                        description=description,
                        done=False,
                        date=date)
        new_task.put()
        values = {'task': new_task}
        return values

  def update_task(self, author, title, description, dones,date):
        if dones == 'true':
          done = True
        else:
          done = False
        task = db.get(self.cid)
        setattr(task, "author", author)
        setattr(task, "title", title)
        setattr(task, "description", description)
        setattr(task, "done", done)
        setattr(task, "date", date)
        task.put()

  def delete_task(self):
        task = db.get(self.cid)
        db.delete(task)
