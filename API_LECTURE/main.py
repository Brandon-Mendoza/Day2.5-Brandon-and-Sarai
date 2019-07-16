#ADD STUFF HERE BRANDON
import webapp2
import random

from google.appengine.api import urlfetch
import json

class MainPage(webapp2.RequestHandler):
    def get(self):
        trivia_endpoint_url = "https://opentdb.com/api.php?amount=1&category=10&difficulty=easy&type=multiple"
        trivia_response= urlfetch.fetch(trivia_endpoint_url).content
        trivia_as_json = json.loads(trivia_response)
        first_result = trivia_as_json['results'][0]
        trivia_question = first_result['question']
        self.response.write(trivia_question)
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
