# Libraries
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail

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

        mail.send_mail(sender="Example.com Support <martafondapascual@gmail.com>",
              to= self.request.get('email'),
              subject="Your account has been approved",
              body="""
                Welcome to TODOListHack

                Thank you and enjoy your tasks

                The todolisthack.com Team
                """)
        self.redirect('/')
