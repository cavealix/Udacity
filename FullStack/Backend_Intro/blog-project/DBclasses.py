#import the db library from GAE
from google.appengine.ext import db

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