import os
import re
import webapp2

signup = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="{{username}}">
          </td>
          <td class="error">
            {{error_username}}
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
            {{error_password}}
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
            {{error_verify}}
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="{{email}}">
          </td>
          <td class="error">
            {{error_email}}
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welcome = """
<!DOCTYPE html>
<html>
    <h1>Welcome, {{username}}!</h1>
</html>
"""


#function for regular expressions for validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(signup)


    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.response.write(signup)
        else:
            self.redirect('/welcome' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(welcome, username = username)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/welcome', Welcome)],
                              debug=True)
