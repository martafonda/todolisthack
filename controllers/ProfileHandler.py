# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

from controllers.UserHandler import UserCrud


class ProfileHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
        values = {'user': user}
        self.response.out.write(template.render('views/profile.html', values))
    else:
        self.redirect('/login')

  def post(self):
        user = users.get_current_user()
        uid = user.user_id()
        crud = UserCrud(uid)

        is_valid = crud.update_user(first_name=self.request.get('first_name'),
                            last_name=self.request.get('last_name'),
                            email=self.request.get('email'))
        self.redirect('/')
