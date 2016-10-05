import os
import jinja2
import webapp2
import re
#Security libararies
import random
import string
import hashlib
import hmac

import time


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
    likes = db.ListProperty(int, default=[0])

#CREATE Blog DB
class Blog(db.Model):
	#string property < 500 char
	title = db.StringProperty(required = True)
	#text property > 500 char
	body = db.TextProperty(required = True)
	#set author id # to user for permissions
	author = db.StringProperty(required = True)
	#number of likes
	likes = db.IntegerProperty()
	#auto set to current time
	created = db.DateTimeProperty(auto_now_add = True)

#CREATE DB for comments
class Comment(db.Model):
	post = db.IntegerProperty(required = True)
	author = db.StringProperty(required = True)
	body = db.StringProperty(required = True)
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
		self.redirect('/blog')

#/BLOG
class BlogHandler(Handler):
	def render_front(self, title='', body='', error=''):
		#query db and display all posts
		posts = db.GqlQuery("select * from Blog order by created desc")
		self.render("blog.html", posts = posts)

	def get(self):
		self.render_front()

#/BLOG/NEWPOST
class NewPostHandler(Handler):
	def get(self):
		self.render('new_post.html')

		#recieve values for new post and add to DB
	def post(self):
		title = self.request.get("title")
		body = self.request.get("body")
		user = user_from_cookie(self)

		#if valid title, body, and user cookie
		if title and body and user:
			#create new instance
			a = Blog(title = title, body = body, author = user.name)
			#store instance
			a.put()
			#get idc

			#redirect to blog post by id
			self.redirect("/blog/%s" % str(a.key().id()))
		else:
			#create error message and prompt user for correct info
			error = "We need both a title and body text"
			self.render("new_post.html", title = title, body = body, error = error)

#POST
class PostHandler(Handler):
	def get(self, pid):
		post = Blog.get_by_id(int(pid))
		#check if post already liked by user
		user = user_from_cookie(self)
		comments = Comment.gql("where post = :post order by created desc", post=int(pid)).fetch(limit=None)

		#set flag if post already liked by user
		if user and int(pid) in user.likes:
			liked = True
		else:
			liked = False
		self.render('post.html', post = post, liked = liked, comments = comments)
	
	def post(self, pid):
		user = user_from_cookie(self)
		body = self.request.get("comment-body")
		comment = Comment(post = int(pid), author = user.name, body = body)
		#store comment
		comment.put()
		time.sleep(.2)
		self.redirect("/blog/%s" % pid)

#/BLOG/SIGNUP
class SignUpHandler(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		#acquire inputs
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		#validate inputs
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
				u = User(name = username, pw = hash_str(password))
				user = u.put()
				uid = user.id()

		#if no errors, redirect to success page
		if name_reply == pass_reply == email_reply == '':
			#set cookie
			self.response.set_cookie('uid', make_secure_val(str(uid)))
			#set global template variable
			jinja_env.globals['user'] = username
			self.redirect("/blog/welcome")
		#else, reload signup page with error replies
		else:
			self.render("signup.html", name = username, name_reply = name_reply, pass_reply = pass_reply, email_reply = email_reply)

#LOGIN
class LoginHandler(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		#acquire inputs
		username = self.request.get("username")
		password = self.request.get("password")

		#check if valid name
		name_reply = vname(username)

		#if valid name entry, query account
		if name_reply == '':
			user = User.gql("where name = :username", username=username).get()
			#if user account exists and correct password, set cookie and redirect
			if user and hash_str(password) == user.pw:
				#set cookie
				self.response.set_cookie('uid', make_secure_val(str(user.key().id())))
				#set global template variable
				jinja_env.globals['user'] = username
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
		user = user_from_cookie(self)
		if user:
			self.render("welcome.html", name = user.name)
		else:
			self.redirect("/blog/login")

#LOGOUT
class LogoutHandler(Handler):
	def get(self):
		uid_cookie = self.request.cookies.get('uid', '')
		if uid_cookie and check_secure_val(uid_cookie):
			self.response.set_cookie('uid', None)
			#set global template variable
			jinja_env.globals['user'] = None
			self.redirect("/blog/signup")
		else:
			self.redirect("/blog/signup")

#Delete
class DeleteHandler(Handler):
	def get(self, pid):
		#check if deleting post or comment
		if Blog.get_by_id(int(pid)):
			post = Blog.get_by_id(int(pid))
			#delete post
			post.delete()
			#remove all comments on post
			comments = Comment.gql("where post = :post", post=int(pid)).fetch(limit=None)
			for comment in comments:
				comment.delete()
			#find all the users who liked the post and remove record
			#users = db.GqlQuery("select * from User where links = :pid", pid=int(pid))
			users = User.all().filter('likes', int(pid)).fetch(limit=None)
			for user in users:
				user.likes.remove(int(pid))
			time.sleep(.2)
			self.redirect('/blog')
		else:
			#delete comment
			comment = Comment.get_by_id(int(pid))
			post_id = comment.post
			comment.delete()
			time.sleep(.2)
			self.redirect('/blog/%s' % post_id)


#Edit
class EditHandler(Handler):
	def get(self, pid):
		#check if edit is for post or comment
		if Blog.get_by_id(int(pid)):
			post = Blog.get_by_id(int(pid))
		else:
			post = Comment.get_by_id(int(pid))
		self.render('edit.html', post = post)

	def post(self, pid):
		#get edited title and body
		#pid = self.request.get("id")
		#check if editing a post or comment and get original post, update, and place back
		if self.request.get("title"):
			title = self.request.get("title")
			body = self.request.get("body")
			post = Blog.get_by_id(int(pid))
			post.title = title
			post.body = body
			post.put()
			time.sleep(.2)
			self.redirect('/blog')
		else:
			body = self.request.get("body")
			comment = Comment.get_by_id(int(pid))
			comment.body = body
			comment.put()
			time.sleep(.2)
			self.redirect('/blog/%s' % comment.post)

class LikeHandler(Handler):
	def get(self, pid):
		user = user_from_cookie(self)
		#if already liked, unlike by removing
		if int(pid) in user.likes:
			user.likes.remove(int(pid))
		#else like by adding to list
		else:
			user.likes.append(int(pid))
		#place updated user back
		user.put()
		#reload page
		self.redirect("/blog/%s" % pid)


#Get user from uid cookie
def user_from_cookie(self):
	uid_cookie = self.request.cookies.get('uid', '')
	if uid_cookie and check_secure_val(uid_cookie):
		uid = uid_cookie.split('|')[0]
		return User.get_by_id(int(uid))

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
							('/blog/([0-9]+)', PostHandler),
							('/blog/signup', SignUpHandler),
							('/blog/welcome', WelcomeHandler),
							('/blog/login', LoginHandler),
							('/blog/logout', LogoutHandler),
							('/blog/delete/([0-9]+)', DeleteHandler),
							('/blog/edit/([0-9]+)', EditHandler),
							('/blog/like/([0-9]+)', LikeHandler)
							], debug=True)