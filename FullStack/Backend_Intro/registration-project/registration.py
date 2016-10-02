import os
import webapp2
import jinja2
import re

secret = 'imsosecret'

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

secret = 'adeaio08a4jnv;lzoia[dpi'

#instantiate database
class Users(db.Model):
	#string property < 500 char
	name = db.StringProperty(required = True)
	#text property > 500 char
	password = db.StringProperty(required = True)
	#auto set to current time
	created = db.DateTimeProperty(auto_now_add = True)

def hash_str(s):
	return hmac.new(secret, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_cal(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

class Handler(webapp2.RequestHandler):
	def write(self, *a, **params):
		self.response.out.write(*a, **params)

		# render template with jinja
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

		# send template back to browser to render
	def render(self, template, **params):
		self.write(self.render_str(template, **params))

class MainPage(Handler):
	def get(self):
		name = self.request.cookies.get('name')
		if uid:
			self.redirect('/welcome')
		else:
			self.redirect('/signup')

class SignUpHandler(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		name_reply = vname(username)
		pass_reply = vpass(password, verify)
		email_reply = vemail(email)

		#if no errors, redirect to success page
		if name_reply == pass_reply == email_reply == '':
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.headers.add_header(('Set-Cookie', 'name=%s Path=/' % username)
			self.redirect('/welcome')
		#else, reload signup page with error replies
		else:
			self.render("signup.html", name = username, name_reply = name_reply, pass_reply = pass_reply, email_reply = email_reply)

class WelcomeHandler(Handler):
	def get(self):
		name = self.request.cookies.get('name', 'visitor')
		self.render('welcome.html', name = name)

#check each input
def vname(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	if USER_RE.match(username):
		return ''
	else:
		return 'Invalid Username'

def vpass(password, verify):
	PASS_RE = re.compile(r"^.{3,20}$")
	if password and verify:
		if (PASS_RE.match(password) and PASS_RE.match(verify)) and (password == verify):
			return ''
		else:
			return 'Invalid Password and Verification'
	else: return 'Password and Verification Required'

def vemail(email):
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
	if not email or EMAIL_RE.match(email):
		return ''
	else:
		return 'Invalid Email'


app = webapp2.WSGIApplication([	('/', MainPage),
								('/signup', SignUpHandler),
								('/welcome', WelcomeHandler)
							], debug=True)