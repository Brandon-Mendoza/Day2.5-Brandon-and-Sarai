import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      if cssi_user:
        self.response.write(
          "Looks like you're registered. Thanks for using our site!")
      else:
        # Registration form for a first-time visitor:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <input type="text" name="first_name">
            <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))

    else:
      # If the user isn't logged in...
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      self.response.write('Please log in.<br>' + login_html_element)


    def post(self):
    user = users.get_current_user()
    # Create a new CSSI user.
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        email=user.nickname())
    # Store that Entity in Datastore.
    cssi_user.put()
    # Show confirmation to the user. Include a link back to the index.
    self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        cssi_user.first_name)


app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
