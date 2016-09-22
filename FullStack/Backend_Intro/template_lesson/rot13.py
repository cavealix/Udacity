import os

import jinja2
import webapp2

# concat path to templates from file location
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# initialize jinja environment and direct paths to template_dir, and autoescape for html entries
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


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)