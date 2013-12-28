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
import os
import datetime
from hashlib import md5

from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import mail
import jinja2
import webapp2
import models
import settings

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader('templates'))

def send_verification(name,email,vcode):
    message = mail.SendMail(sender="",
                            subject="Account verification instructions for teamsaround.appspot.com",
                            to="%s <%s>" % (name,email),
                            body=""" Hello %s!
    
    Thank you for registering with Teamsaround! You are just one step away from finding a team for your favorite sport.
    Please log in to teamsaround.appspot.com and click on the registrationlink in this mail to complete your registration.
    If for some reason the link doesn't work, open your browser and copy the link to the address bar.
    Please don't forget to log in before using the verification link!
                            
    http://teamsaround.appspot.com/verification?vcode=%s
    
    Enjoy!""" % (name,vcode))

def validate(self, **kwargs):
    pass

def render_template(self, template, template_values):
    page = jinja_environment.get_template(template)
    self.response.out.write(page.render(template_values))

def encrypt(txt):
    return md5(txt).hexdigest()
    
def dont_verify(fn):
    def wrapper(self):
        return(fn)
    wrapper
    
def owners_only(fn):
    def wrapper(self):
        roles = self.user.role
        if "owner" in roles:
            return fn(self)
        else:
            self.response.out.write("This page is for the owners only. You have a place to rent out? Register your account as an owner here.")
    
    return wrapper
        
        
def login_required(fn):
    '''So we can decorate any RequestHandler with @login_required'''
    
    def wrapper(self):
        session = Session(self.request)
        user = None
        
        if session.valid == True:
            user = models.Users.get_by_id(session.email)
            self.user = user # Passing the user with the request (so we don't have to query again to get it's properties)
        else:
            self.redirect('/login')
  
        if user:
            # unverifed_access is a list of paths which are made accessible without user verification. Required by the "/verification" for example.
            if user.verified == True or self.request.path in settings.unverified_access:
                # this line returns the handler for the request.. 
                return fn(self)
            else:
                self.redirect('/verification')
        else:
            self.redirect('/login')
              
    return wrapper

class Session(object):
    '''Creates a session object, which contains all the info about a session from the memcache or the datastore.
       If a stored session for the required SID wasn't found, the valid property is set to False.
       Also provides methods to modify values in the session, create new session, or delete a session.'''
    
    def remove(self):
        memcache.delete(self.sid)

    
    def set(self,email):
        
        ip = self.request.remote_addr   # get our client's ip address. 
             
        sid = md5(os.urandom(256)).hexdigest()
        exp = datetime.datetime.now() + datetime.timedelta(seconds= settings.session_expiration)
        expires = exp.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.request.response.headers.add_header('Set-Cookie', 'sid = %s; expires = %s' % (sid, expires))       
        memcache.add(sid, {'email':email,'ip':ip,'expires':expires}, settings.session_expiration)

    def __init__(self,request):
        
        self.request = request
        self.valid = False
        clientsid = request.cookies.get('sid')
        clientsip = request.remote_addr
        
        if clientsid == None:
            self.ip = self.sid = self.email = self.valid = None
            return

        session = memcache.get(clientsid)
        if session != None:
            self.ip = session['ip']
            self.sid = clientsid
            self.email = session['email']
            self.valid = True


class RegistrationHandler(webapp2.RequestHandler):
    '''Processes the registration form'''
        
    def post(self):
        email = self.request.get("email")
        name = self.request.get("name")
        password = self.request.get("password")
        password2 = self.request.get("password2")
        
        if '' in (email, name, password, password2):
            self.redirect('/login?error=All+fields+are+required.')
        else:
            if password == password2:                               # if the two passwords match,
                if models.Users.get_by_id(email) == None:           # If there is no such user,we can proceed
                    user = models.Users(id=email,                   # using the email as the ID for users. (so we can perform cheaper "get_by_id" retrievals)
                                        email=email,
                                        name=name,
                                        password=encrypt(password),
                                        verified=False,
                                        vcode=encrypt(os.urandom(256)),
                                        role=['player'])
                    #user.add_role('owner') # test if it works
                    user.put()
                    send_verification(name,email,user.vcode)    # send the welcome-verification email
                    session = Session(self.request)             # and also set a session for the current user so they can go on with the verification
                    session.set(email)
                    self.redirect('/verification')
                else:
                    self.redirect('/login?error=This+email+is+already+registered.')
            else:
                self.redirect('/login?error=Passwords+must+be+identical.')

class VerificationHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        self.vcode = self.request.get('vcode')
        session = Session(self.request)
        
        user = models.Users.get_by_id(session.email)
        if user == None:
            self.response.out.write("The user you are about to verify doesn't exist anymore.")
        if self.vcode == user.vcode:
            user.verified = True
            user.vcode = None
            user.put()

        template = 'verify.html'
        template_values = {'error': self.request.get('error'),
                           'verified': user.verified,
                           'name': user.name}
        render_template(self,template,template_values)
        

    @login_required
    def post(self):        
        vcode = self.request.get('vcode')
        query = models.Users.all()
        query.filter('vcode =', vcode)
        result = query.get()
        if result != None:
            result.verified = True
            result.put()
            self.redirect('/')
        else:
            self.redirect('/verification?error= %s ' % email)
            

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        error = self.request.get("error")
        template = 'login.html'
        template_values = {'error' : error}
        render_template(self,template,template_values)
    def post(self):
        email = self.request.get("email",default_value=None)
        pwd = self.request.get("password",default_value=None)
        if email == '' or pwd == '':
            self.redirect('/login?error=Email+and+password+are+required.')
            return

        user = models.Users.get_by_id(email)
        password = md5(pwd).hexdigest()         

        if user:
            if user.password == password:
                if user.verified != True:
                    isverified = False
                    target = '/verification'
                    self.redirect('/verification')
                else:                        
                    target = '/'
                    isverified = True
                    
                session = Session(self.request)
                session.set(email)
                self.redirect(target)
            else:
                self.redirect('/login?error=Invalid+username+or+password.')

        else:
            self.redirect('/login?error=Invalid+username+or+password.')


class LogoutHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        session = Session(self.request)
        session.remove()
        self.response.headers.add_header('Set-Cookie', 'sid=None; expires=%s' % (datetime.datetime.now()))
        self.redirect('/')


class MainPage(webapp2.RequestHandler):
    """docstring for MainPage"""
    @login_required
    def get(self):
        template = 'welcome.html'
        template_values = ''
        render_template(self,template,template_values)

    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/welcome', LoginHandler),
    ('/registration', RegistrationHandler),
    ('/verification', VerificationHandler),
    ('/test', TestHandler),
    ], debug = True)
