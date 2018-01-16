import webapp2
import os
import jinja2
from google.appengine.ext import db 

template_dir=os.path.dirname(__file__)
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)
	def render_str(self,template,**params):
		t=jinja_env.get_template(template)
		return t.render(params)
	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))

class ART(db.Model):
	title=db.StringProperty()
	arttype=db.TextProperty()
	created=db.DateTimeProperty(auto_now_add=True)

class mainpage(handler):
	def render_form(self,title="",art="",error=""):
		x=db.GqlQuery('SELECT * from ART')
		arts=db.GqlQuery("SELECT * from ART ORDER BY created desc")
		self.render('form.html',title_text=title,arttext=art,error=error,arts=arts)
	
	def get(self):
		self.render_form()

	def post(self):
		error=""
		title=self.request.get('Title')
		art=self.request.get('art')
		if title and art:
			a=ART(title=title,arttype=art)
			a.to_put()
			self.redirect('/')
		else:
			error="* Oops both fields are mandatory"
			self.render('form.html',title_text=title,arttext=art,error=error)

app=webapp2.WSGIApplication([('/',mainpage)],debug=True)
