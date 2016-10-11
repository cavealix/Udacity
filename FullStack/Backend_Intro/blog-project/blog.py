import os
import jinja2
import webapp2
import re
import time

# Custom modules
import security
import DBclasses

# import the db library from GAE
from google.appengine.ext import db

# concat path to templates from file location
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# initialize jinja environment and direct paths to template_dir
jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


# PARENT HANDLER
class Handler(webapp2.RequestHandler):
	def write(self, *a, **params):
		self.response.out.write(*a, **params)

	#render template with jinja
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	#send template back to browser to render
	def render(self, template, **params):
		self.write(self.render_str(template, **params))


# MAIN PAGE
class MainPage(Handler):
	def get(self):
		self.redirect('/blog')


# /BLOG
class BlogHandler(Handler):
	def render_front(self, title='', body='', error=''):
		#query db and display all posts
		posts = db.GqlQuery("select * from Blog order by created desc")
		self.render("blog.html", posts=posts)

	def get(self):
		self.render_front()


# /BLOG/NEWPOST
class NewPostHandler(Handler):
	def get(self):
		#if user not logged in redirect to login page
		if user_from_cookie(self):
			self.render('new_post.html')
		else:
			self.redirect('/blog/login')

	#recieve values for new post and add to DB
	def post(self):
		title = self.request.get("title")
		body = self.request.get("body")
		user = user_from_cookie(self)

		if user:
			#if valid title, body, and user cookie
			if title and body:
				#create new instance
				a = DBclasses.Blog(title=title, body=body, author=user.name)
				#store instance
				a.put()
				#get idc
	
				#redirect to blog post by id
				self.redirect("/blog/%s" % str(a.key().id()))
			else:
				#create error message and prompt user for correct info
				error = "We need both a title and body text"
				self.render("new_post.html", title=title, body=body, error=error)
		else:
			#create error message and prompt user for correct info
			error = "Please login to post a new article"
			self.render("new_post.html", title=title, body=body, error=error)


# POST
class PostHandler(Handler):
	def get(self, pid):
		post = DBclasses.Blog.get_by_id(int(pid))
		#check if post already liked by user
		user = user_from_cookie(self)
		comments = DBclasses.Comment.gql(
			"where post = :post order by created desc",
			post=int(pid)).fetch(limit=None)

		#set flag if post already liked by user
		if user and int(pid) in user.likes:
			liked = True
		else:
			liked = False
		self.render('post.html', post=post, liked=liked, comments=comments)
	
	def post(self, pid):
		user = user_from_cookie(self)
		body = self.request.get("comment-body")
		comment = DBclasses.Comment(post=int(pid), author=user.name, body=body)
		#store comment
		comment.put()
		time.sleep(.2)
		self.redirect("/blog/%s" % pid)


# /BLOG/SIGNUP
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
		name_reply = security.vname(username)
		pass_reply = security.vpass(password, verify)
		email_reply = security.vemail(email)

		#if valid name, check if already in User db
		if name_reply == '':
			#if name already exists, set error message
			user = DBclasses.User.gql("where name = :username", username=username).get()
			if user:
				name_reply = "Name %s already exists" % user.name
			#else store entry in User db
			else:
				u = DBclasses.User(name=username, pw=security.hash_str(password))
				user = u.put()
				uid = user.id()

		#if no errors, redirect to success page
		if name_reply == pass_reply == email_reply == '':
			#set cookie
			self.response.set_cookie('uid', security.make_secure_val(str(uid)))
			#set global template variable
			jinja_env.globals['user'] = username
			self.redirect("/blog/welcome")
		#else, reload signup page with error replies
		else:
			self.render("signup.html", name=username, name_reply=name_reply,
				pass_reply=pass_reply, email_reply=email_reply)


# LOGIN
class LoginHandler(Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		#acquire inputs
		username = self.request.get("username")
		password = self.request.get("password")

		#check if valid name
		name_reply = security.vname(username)

		#if valid name entry, query account
		if name_reply == '':
			user = DBclasses.User.gql("where name = :username", username=username).get()
			#if user account exists and correct password, set cookie and redirect
			if user and security.hash_str(password) == user.pw:
				#set cookie
				self.response.set_cookie(
					'uid', security.make_secure_val(str(user.key().id())))
				#set global template variable
				jinja_env.globals['user'] = username
				self.redirect("/blog/welcome")
			else:
				self.render("login.html", name=username,
						name_reply='Invalid Credentials')
		#else, reload signup page with error replies
		else:
			self.render("login.html", name=username, name_reply=name_reply)


# SIGN UP SUCCESS - WELCOME
class WelcomeHandler(Handler):
	def get(self):
		#find user from db by id
		user = user_from_cookie(self)
		if user:
			self.render("welcome.html", name=user.name)
		else:
			self.redirect("/blog/login")


# LOGOUT
class LogoutHandler(Handler):
	def get(self):
		uid_cookie = self.request.cookies.get('uid', '')
		if uid_cookie and security.check_secure_val(uid_cookie):
			self.response.set_cookie('uid', None)
			#set global template variable
			jinja_env.globals['user'] = None
			self.redirect("/blog/login")
		else:
			self.redirect("/blog/signup")


# Delete
class DeleteHandler(Handler):
	def get(self, pid):
		#check authentication and authorization
		if DBclasses.Blog.get_by_id(int(pid)).author == \
								user_from_cookie(self).name:
			#check if deleting post or comment
			if DBclasses.Blog.get_by_id(int(pid)):
				post = DBclasses.Blog.get_by_id(int(pid))
				#delete post
				post.delete()
				#remove all comments on post
				comments = DBclasses.Comment.gql(
					"where post = :post", post=int(pid)).fetch(limit=None)
				for comment in comments:
					comment.delete()
				#find all the users who liked the post and remove record
				users = DBclasses.User.all().filter(
							'likes', int(pid)).fetch(limit=None)
				for user in users:
					user.likes.remove(int(pid))
				time.sleep(.2)
				self.redirect('/blog')
			else:
				#delete comment
				comment = DBclasses.Comment.get_by_id(int(pid))
				post_id = comment.post
				comment.delete()
				time.sleep(.2)
				self.redirect('/blog/%s' % post_id)
		else:
			self.redirect('/blog')


# Edit
class EditHandler(Handler):
	def get(self, pid):
		#check authentication and authorization
		if DBclasses.Blog.get_by_id(int(pid)).author == \
								user_from_cookie(self).name:
			#check if edit is for post or comment
			if DBclasses.Blog.get_by_id(int(pid)):
				post = DBclasses.Blog.get_by_id(int(pid))
			else:
				post = DBclasses.Comment.get_by_id(int(pid))
			self.render('edit.html', post=post)
		else:
			self.redirect('/blog')

	def post(self, pid):
		#check authentication and authorization
		if DBclasses.Blog.get_by_id(int(pid)).author == \
								user_from_cookie(self).name:
			#if edit canceled, return to post page
			if self.request.get("cancel"):
				self.redirect("/blog")
			else:		
				#check if editing a post or comment and get 
					#original post, update, and place back
				if self.request.get("title"):
					title = self.request.get("title")
					body = self.request.get("body")
					post = DBclasses.Blog.get_by_id(int(pid))
					post.title = title
					post.body = body
					post.put()
					time.sleep(.2)
					self.redirect('/blog')
				else:
					body = self.request.get("body")
					comment = DBclasses.Comment.get_by_id(int(pid))
					comment.body = body
					comment.put()
					time.sleep(.2)
					self.redirect('/blog/%s' % comment.post)
		else:
			self.redirect('/blog')


class LikeHandler(Handler):
	def get(self, pid):
		user = user_from_cookie(self)
		#make sure users can't like their own post
		if DBclasses.Blog.get_by_id(int(pid)).author != user:
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
		else:
			self.redirect('/blog')


# Get user from uid cookie
def user_from_cookie(self):
	uid_cookie = self.request.cookies.get('uid', '')
	if uid_cookie and security.check_secure_val(uid_cookie):
		uid = uid_cookie.split('|')[0]
		return DBclasses.User.get_by_id(int(uid))


# HANDLER REDIRECTS
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
