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

import webapp2
import cgi
import string
import cgitb

form = """<!DOCTYPE html>
<html>
  <head>
    <title>
      Unit-2-Rot13 by Suhas
    </title>
  </head>
  
  <body>
    <h2>
      Enter text below to ROT13:
    </h2>
    <form method="post">
      <textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>
</html>"""

def escape_html(s):
	return cgi.escape(s, quote=True)

def rot13(s):
	abc = string.ascii_lowercase
	abc_13 = abc[13:] + abc[:13]
	rot_13 = ''

	for c in s:
		if c in string.ascii_letters:
			rot_13 += abc_13[abc.index(c.lower())]
		else:
			rot_13 += c

	for i in range(0, len(s)):
		if s[i] in string.ascii_uppercase:
			rot_13 = rot_13.replace(rot_13[i], rot_13[i].upper())

	return rot_13

class Rot13(webapp2.RequestHandler):
    def write_form(self, text=""):
    	self.response.out.write(form %{"text" : escape_html(text)})

    def get(self):
    	self.write_form()

    def post(self):
    	input = self.request.get("text")
    	encoded_text = rot13(input)
        if encoded_text:
    		self.write_form(encoded_text)
    	else:
    		self.write_form('')

	


app = webapp2.WSGIApplication([
    ('/', Rot13)
], debug=True)







