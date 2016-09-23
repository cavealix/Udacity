import os
import jinja2
import webapp2

#import the db library from GAE
from google.appengine.ext import db

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

#instantiate database
class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	#auto set to current time
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def render_front(self, title='', art='', error=''):
		#query db
		arts = db.GqlQuery("select * from Art order by created desc")

		self.render("front.html", title = title, art = art, error = error, arts = arts)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			#create new instance
			a = Art(title = title, art = art)
			#store instance
			a.put()

			#redirect to home
			self.redirect("/")
		else:
			error = "We need both a title and some artwork"
			self.render_front(title, art, error)


app = webapp2.WSGIApplication([	('/', MainPage)
							], debug=True)