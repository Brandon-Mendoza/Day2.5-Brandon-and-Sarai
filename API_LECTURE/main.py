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
        correct_answer = first_result['correct_answer']
        incorrect_answers = first_result['incorrect_answers']

        all_answer_options = [correct_answer]
        for answer in incorrect_answers:
            all_answer_options.append(answer)

        random.shuffle(all_answer_options)

        self.response.write("<h2>" + trivia_question + "</h2>")
        self.response.write(all_answer_options)





app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
