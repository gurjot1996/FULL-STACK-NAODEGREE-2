import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir=os.path.dirname(__file__)
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape= True)

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
    content=db.StringProperty()
    created=db.DateTimeProperty(auto_now_add=True)


class mainpage(handler):
    def get(self):
        self.redirect('/blog/new')

class newblog(handler):
    def get(self):
        self.render('newblog.html')
    def post(self):
        error=""
        title=self.request('title')
        content=self.request('content')
        if title and content:
            entry=Database(title=title,content=content)
            entry.put()
            self.redirect('/blog/%s'%str(entry.key().id()))
        else:
            error="both fields are mandatory"
            self.render('newblog.html',error=error)







app=webapp2.WSGIApplication([('/',mainpage),('/blog',blogpage),('/blog/[0-9]+',newentry),('/blog/new',newblog)],debug=True)