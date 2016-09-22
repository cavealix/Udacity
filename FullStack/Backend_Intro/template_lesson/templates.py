import os

import jinja2
import webapp2

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

app = webapp2.WSGIApplication([	('/', MainPage),
								('/fizzbuzz', FizzBuzzHandler)
							], debug=True)