import os

import jinja2
import webapp2
import re

# concat path to templates from file location
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# initialize jinja environment and direct paths to template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

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
		# self.request.get_all() is a function that returns a list of all values that belong to string that matches a key in our query parameter 
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)

class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render('fizzbuzz.html', n = n)

class Rot13Handler(Handler):
	def get(self):
		self.render("rot13.html")

	def post(self):
		# self.request.get_all() is a function that returns a list of all values that belong to string that matches a key in our query parameter 
		text = self.request.get("text")
		self.render("rot13.html", code = check(text))

def check(text):
		s = list(text)
		for c in range (0, len(s)):
			if s[c].isalpha():
				n = ord(s[c])
				if (n >= 97) and (n <= 109):
					n = n + 13
					s[c] = chr(n)
				elif (n >= 110) and (n <= 122):
					n = n - 13
					s[c] = chr(n)
				elif (n >= 65) and (n <= 77):
					n = n + 13
					s[c] = chr(n)
				elif (n >= 78) and (n <= 90):
					n = n - 13
					s[c] = chr(n)
		return ''.join(s)

class SignUpHandler(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		username = self.request.get("username")
		pass1 = self.request.get("pass1")
		pass2 = self.request.get("pass2")
		email = self.request.get("email")

		name_reply = vname(username)
		pass_reply = vpass(pass1, pass2)
		email_reply = vemail(email)

		#if no errors, redirect to success page
		if name_reply == pass_reply == email_reply == '':
			self.redirect("/success?name=" + username)
		#else, reload signup page with error replies
		else:
			self.render("signup.html", name = username, name_reply = name_reply, pass_reply = pass_reply, email_reply = email_reply)

#check each input
def vname(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	if USER_RE.match(username):
		return ''
	else:
		return 'Invalid Username'

def vpass(pass1, pass2):
	PASS_RE = re.compile(r"^.{3,20}$")
	if pass1 and pass2:
		if (PASS_RE.match(pass1) and PASS_RE.match(pass2)) and (pass1 == pass2):
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
		
	

class SuccessHandler(Handler):
	def get(self):
		name = self.request.get("name")
		self.render("signup_success.html", name = name)


app = webapp2.WSGIApplication([	('/', MainPage),
								('/fizzbuzz', FizzBuzzHandler), 
								('/rot13', Rot13Handler),
								('/signup', SignUpHandler),
								('/success', SuccessHandler)
							], debug=True)