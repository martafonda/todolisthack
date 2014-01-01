# Libraries
from google.appengine.ext import db
import webapp2
#  Database Model
class Task(db.Model):
  author = db.EmailProperty(required=True)
  title = db.StringProperty(required=True)
  description = db.StringProperty(multiline=True, required=True)
  date = db.DateTimeProperty(auto_now_add=True)

class SearchHandler(webapp2.RequestHandler):
  user_list = db.GqlQuery( 'SELECT * FROM User')