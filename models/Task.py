# Libraries
from google.appengine.ext import db
#  Database Model
class Task(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)