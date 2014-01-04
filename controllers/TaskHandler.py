#!/usr/bin/env python
# Libraries
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
import webapp2
import datetime
import logging

#Models
from models.Task import Task

class TaskHandler(webapp2.RequestHandler):
  def get(self):
    #Searching users in memcache
    user_list = self.get_users()
    current_user = users.get_current_user()
    crud = TaskCrud(self.request.get('id'))
    user_tasks = crud.retrieve_tasks()
    values = {'users' : user_list, 
              'logout_url': users.create_logout_url("/"), 
              'tasks': user_tasks,
              'user': current_user}
    self.response.out.write(template.render('views/main.html', values))
  
  def get_users(self):
    users = memcache.get("users")
    if users is not None:                     #If there are users in memcache
      return users
    else:                                     #If there aren't users in memcache
      users = self.retrieve_users()           #Get them from DB
      if not memcache.add("users", users, 10):#Save them into memcache
          logging.error("Memcache set failed.")
      return users
  
  def retrieve_users(self):
    return db.GqlQuery( 'SELECT * FROM User')

  def post(self):
    tid = self.request.get('id')
    crud = TaskCrud(tid)
    date = self.request.get('date')
    date_parsed = datetime.datetime.strptime(date, '%m/%d/%Y').date()
    if tid:#If the task already exists
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

  def retrieve_tasks(self):
    current_user = users.get_current_user()
    user_email = current_user.email()
    return db.GqlQuery( "SELECT * FROM Task WHERE author = :1 ORDER BY date",
                         user_email)
  
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
