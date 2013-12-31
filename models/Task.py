# Libraries
from google.appengine.ext import db
#  Database Model
class Task(db.Model):
    uid = db.StringProperty(required=True)
    author = db.EmailProperty(required=True)
    content = db.StringProperty(multiline=True, required=True)
    date = db.DateTimeProperty(auto_now_add=True)