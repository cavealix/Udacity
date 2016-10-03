import os
import jinja2
import webapp2
import re
#Security libararies
import random
import string
import hashlib
import hmac


#import the db library from GAE
from google.appengine.ext import db

# concat path to templates from file location
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# initialize jinja environment and direct paths to template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


#CREATE User DB
class User(db.Model):
    name = db.StringProperty(required = True)
    pw = db.StringProperty(required = True)

#CREATE Blog DB
class Blog(db.Model):
	#string property < 500 char
	title = db.StringProperty(required = True)
	#text property > 500 char
	body = db.TextProperty(required = True)
	#auto set to current time
	created = db.DateTimeProperty(auto_now_add = True)


#PARENT HANDLER
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

#MAIN PAGE
class MainPage(Handler):
	def get(self):
		self.redirect('/blog/signup')

#/BLOG
class BlogHandler(Handler):
	def render_front(self, title='', body='', error=''):
		#query db
		posts = db.GqlQuery("select * from Blog order by created desc")

		self.render("blog.html", posts = posts)

	def get(self):
		self.render_front()

#/BLOG/NEWPOST
class NewPostHandler(Handler):
	def get(self):
		self.render('new_post.html')

	def post(self):
		title = self.request.get("title")
		body = self.request.get("body")

		if title and body:
			#create new instance
			a = Blog(title = title, body = body)
			#store instance
			a.put()
			#get idc

			#redirect to blog post by id
			self.redirect("/blog/%s" % str(a.key().id()))
		else:
			#create error message and prompt user for correct info
			error = "We need both a title and body text"
			self.render("new_post.html", title = title, body = body, error = error)

#POSTID
class PostIDHandler(Handler):
	def get(self, pid):
		#url = self.request.path
		#pid = re.search('([0-9]+)', url)

		post = Blog.get_by_id(int(pid))
		self.render('post.html', post = post)

#/BLOG/SIGNUP
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

		#if valid name, check if already in User db
		if name_reply == '':
			#if name already exists, set error message
			#user = db.GqlQuery("select * from User where name = :username", username=username)
			user = User.gql("where name = :username", username=username).get()
			if user:
				name_reply = "Name %s already exists" % user.name
			#else store entry in User db
			else:
				u = User(name = username, pw = password)
				user = u.put()
				uid = user.id()

		#if no errors, redirect to success page
		if name_reply == pass_reply == email_reply == '':
			self.response.set_cookie('uid', make_secure_val(str(uid)))
			self.redirect("/blog/welcome")
		#else, reload signup page with error replies
		else:
			self.render("signup.html", name = username, name_reply = name_reply, pass_reply = pass_reply, email_reply = email_reply)

#LOGIN
class LoginHandler(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")

		name_reply = vname(username)

		#if valid name entry, query account
		if name_reply == '':
			user = User.gql("where name = :username", username=username).get()
			#if user account exists and correct password, set cookie and redirect
			if user and password == user.pw:
				self.response.set_cookie('uid', make_secure_val(str(user.key().id())))
				self.redirect("/blog/welcome")
			else:
				self.render("login.html", name = username, name_reply = 'Invalid Credentials')
		#else, reload signup page with error replies
		else:
			self.render("login.html", name = username, name_reply = name_reply)

#SIGN UP SUCCESS - WELCOME
class WelcomeHandler(Handler):
	def get(self):
		#find user from db by id
		uid_cookie = self.request.cookies.get('uid', '')
		if check_secure_val(uid_cookie):
			#seperate name from hash, 'name|hash'
			uid = uid_cookie.split('|')[0]
			user = User.get_by_id(int(uid))
			self.render("welcome.html", name = user.name)

#LOGOUT
class LogoutHandler(Handler):
	def get(self):
		uid_cookie = self.request.cookies.get('uid', '')
		if uid_cookie and check_secure_val(uid_cookie):
			self.response.set_cookie('uid', None)
			self.redirect("/blog/signup")
		else:
			self.redirect("/blog/signup")


#SECURITY
SECRET = 'imsosecret'
#Hash
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()
#Make Secure Cookie
def make_secure_val(uid):
    return "%s|%s" % (uid, hash_str(uid))
#Check Cookie
def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


#VERIFY EACH INPUT
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
		

#HANDLER REDIRECTS
app = webapp2.WSGIApplication([	('/', MainPage),
							('/blog', BlogHandler),
							('/blog/newpost', NewPostHandler),
							#anything passed in () is read as a parameter, pid
							('/blog/([0-9]+)', PostIDHandler),
							('/blog/signup', SignUpHandler),
							('/blog/welcome', WelcomeHandler),
							('/blog/login', LoginHandler),
							('/blog/logout', LogoutHandler)
							], debug=True)