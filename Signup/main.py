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

class Database(db.Model):
	title=db.StringProperty()
	content=db.TextProperty()
	created=db.DateTimeProperty(auto_now_add=True)
	modified=db.DateTimeProperty(auto_now=True)

class mainpage(handler):
	def get(self):
		data=Database.all().order('-created')
		self.render('mainpage.html',data=data)



class newentrypage(handler):
	def get(self):
		self.render('signup.html')
	def post(self):
		error=""
		title=self.request.get('title')
		content=self.request.get('content')
		if title and content:
			a=Database(title=title,content=content)
			a.put()
			self.redirect('/blogs/%s'%str(a.key().id()))
		else:
			error="***both fields are mandatory***"
			self.render('signup.html',error=error)

class blogpage(handler):
	def get(self,post_id):
		key=db.Key.from_path('Database',int(post_id))
		data=db.get(key)
		self.render("mainpage.html",data=data)

app=webapp2.WSGIApplication([('/blogs',mainpage),('/blogs/[0-9]+',blogpage),('/blogs/newentry',newentrypage)],debug=True)
