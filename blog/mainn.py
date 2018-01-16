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


title_info="Enter title for blog"
content_info="Enter blog content"

class newblog(handler):
    def get(self):
        self.render('newblog.html',pagename="Signup",title=title_info,content=content_info)
    def post(self):
        error=""
        title=self.request.get('title')
        content=self.request.get( 'content')
        if title<>title_info and content<>content_info and title and content:
            entry=Database(title=title,content=content)
            entry.put()
            self.redirect('/blog/%s'%str(entry.key().id()))
        else:
            error="***both fields are mandatory***"
            self.render('newblog.html',error=error,pagename="Sinup",title=title,content=content)


class blogpage(handler):
    def get(self):
        data=db.GqlQuery('SELECT *  FROM Database ORDER BY created DESC LIMIT 10')
        self.render('blogpage.html',pagename="Blog's",data=data)

class newentry(handler):
    def get(self,post_id):
        key=db.Key.from_path('Database',int(post_id))
        data=db.get(key)
        self.render('newentry.html',pagename="Blog's",linker="/blog",x=data)



app=webapp2.WSGIApplication([('/',mainpage),('/blog',blogpage),('/blog/([0-9]+)',newentry),('/blog/new',newblog)],debug=True)