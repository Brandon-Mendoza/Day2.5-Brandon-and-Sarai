#ADD STUFF HERE BRANDON
import webapp2

from google.appengine.api import urlfetch
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello World")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
