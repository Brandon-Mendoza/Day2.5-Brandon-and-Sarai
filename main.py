import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

class CssiUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

class SecretHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      if cssi_user:
        self.response.write("You found the secret content!")
        return
    self.error(403)
    return

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      if cssi_user:
        self.response.write('''
          Welcome %s %s (%s)! <br> %s <br>''' % (
          cssi_user.first_name,
          cssi_user.last_name,
          email_address,
          signout_link_html)
          )
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
        if not user:
      # You shouldn't be able to get here without being logged in
      self.redirect('/')
    else:
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
  ('/', MainHandler),
  ('/classified', SecretHandler)
], debug=True)
