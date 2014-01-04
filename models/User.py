#!/usr/bin/env python
# Libraries
from google.appengine.ext import db

#  Database Model
class User(db.Model):
    uid = db.StringProperty(required=True)
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    validated = db.BooleanProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)