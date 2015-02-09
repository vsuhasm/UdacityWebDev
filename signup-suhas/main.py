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
import cgi
import re

form = """
<h2>Signup, please! :-)</h2>
<form method="post">
  <table>
    <tr>
      <td class="label">
        Username
      </td>
      <td>
        <input type="text" name="username" value="%(username)s">
      </td>
      <td class="error">
        <span style="color: red">%(user_err)s</span>
      </td>
    </tr>

    <tr>
      <td class="label">
        Password
      </td>
      <td>
        <input type="password" name="password" value="">
      </td>
      <td class="error">
        <span style="color: red">%(password_err)s</span>
      </td>
    </tr>

    <tr>
      <td class="label">
        Verify Password
      </td>
      <td>
        <input type="password" name="verify" value="">
      </td>
      <td class="error">
        <span style="color: red">%(verify_err)s</span>
      </td>
    </tr>

    <tr>
      <td class="label">
        Email (optional)
      </td>
      <td>
        <input type="text" name="email" value="%(email)s">
      </td>
      <td class="error">
        <span style="color: red">%(email_err)s</span>
      </td>
    </tr>
  </table>

  <input type="submit">
</form>
"""
def escape_html(s):
	return cgi.escape(s, quote=True)

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
pass_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_user(username):
	return user_re.match(username)

def valid_pass(password):
	return pass_re.match(password)

def valid_email(email):
	return email_re.match(email)

def valid_verify(p1,p2):
    if(p1 == p2):
        return p1

class MainHandler(webapp2.RequestHandler):
    def write_form(self,username="",email="",user_err="",
                   password_err="",verify_err="",email_err=""):
        self.response.out.write(form % {"username": escape_html(username),
                                        "user_err": user_err,
                                        "password_err": password_err,
                                        "verify_err": verify_err,
                                        "email": escape_html(email),
                                        "email_err": email_err})
                                        
    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        user_err = ""
        password_err = ""
        email_err = ""
        verify_err = ""

        user = valid_user(username)
        passw = valid_pass(password)
        emai = valid_email(email)
        ver = valid_verify(password,verify)

        if not user:
            user_err = "That ain't a valid user name. Please enter again."

        if not passw:
            password_err = "That ain't a valid passowrd. Please enter again."

        if (passw and (not ver)):
            verify_err = "Your passwords don't seem to match. Please enter again"

        if (email and (not emai)):
            email_err = "That's not a valid user email."

        if (not (user and passw and ver)) or (email and (not emai)):
            self.write_form(username,email,user_err,password_err,verify_err,email_err)
        else:
            self.redirect("/welcome?username=%s" % escape_html(username))

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.write("Welcome, " + username)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/welcome', WelcomeHandler)],
                              debug=True)		
