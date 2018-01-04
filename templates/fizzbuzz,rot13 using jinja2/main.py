import webapp2
import jinja2
import os


template_dir=os.path.dirname(__file__)
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

hidden_html="""
<input type="hidden" value="%s" name="food">
"""

list_item="""
<li>%s</li>
"""

shopping_list="""
<h1 >Shopping list
<ul>
%s
</ul>
"""

class handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**param):
		t=jinja_env.get_template(template)
		return t.render(param)

	def render(self,template,**kw):
			self.write(self.render_str(template,**kw))

class mainpage(handler):
	def get(self):
		self.response.out.write("hello")
		self.redirect("/fizzbuzz")
		# output=form_html
		# output_hidden=""
		# output_item=""
		# output_shopping=""
		# items=self.request.get_all('food')
		# for item in items:
		# 	output_hidden+=hidden_html % item
		# 	output_item+=list_item % item

		# output_shopping=shopping_list % output_item
		# output+=output_shopping
		# output=output % output_hidden
		# self.write(output)
class fizzbuzz(handler):
	def get(self):
		m=int(self.request.get('n',10))
		self.render('form_main.html',n=m)

app=webapp2.WSGIApplication([('/',mainpage),('/fizzbuzz',fizzbuzz)],debug=True)