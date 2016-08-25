import webapp2
import re
import cgi

signup = """
<!DOCTYPE html>

<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
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
<body>
  <h2>Welcome, %(username)s!</h2>
</body>
</html>
"""

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

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
        response = signup + error_element
        self.response.write(response)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        username = cgi.escape(username, quote=True)
        password = cgi.escape(password, quote=True)
        verify = cgi.escape(verify, quote=True)


        if email != "":
            email = cgi.escape(email, quote=True)

        if not valid_username(username):
            error = "Invalid Username"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        if not valid_password(password):
            error = "Invalid password"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        elif password != verify:
            error = "Passwords not the same"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)

        if not valid_email(email):
            error = "Not a valid email"
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)


        username = self.request.get("username")
        self.response.write(welcome % {"username": username})


app = webapp2.WSGIApplication([
        ('/', Signup)
], debug=True)
