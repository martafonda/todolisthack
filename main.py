#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import mail

from controllers.LoginHandler import LoginHandler
from controllers.ProfileHandler import ProfileHandler
from controllers.SignUpHandler import SignUpHandler
from controllers.NewTaskHandler import NewTaskHandler
from controllers.TaskHandler import TaskCrud, TaskHandler
from controllers.DeleteTaskHandler import DeleteTaskHandler


class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      self.redirect('/task')
    else:
      self.redirect('/login')

app = webapp2.WSGIApplication([
    webapp2.Route(r'/task', TaskHandler),
    webapp2.Route(r'/new_task', NewTaskHandler),
    webapp2.Route(r'/delete_task', DeleteTaskHandler),
    webapp2.Route(r'/login', LoginHandler, name = 'login'),
    webapp2.Route(r'/sign_up', SignUpHandler),
    webapp2.Route(r'/profile', ProfileHandler),
    webapp2.Route(r'/', MainHandler)
  ], debug=True)
