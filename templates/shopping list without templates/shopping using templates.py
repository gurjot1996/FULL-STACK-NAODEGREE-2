import webapp2
import jinja2
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

class mainpage(handler):
	def get(self):
		output=form_html
		output_hidden=""
		output_item=""
		output_shopping=""
		items=self.request.get_all('food')
		for item in items:
			output_hidden+=hidden_html % item
			output_item+=list_item % item

		output_shopping=shopping_list % output_item
		output+=output_shopping
		output=output % output_hidden
		self.write(output)

app=webapp2.WSGIApplication([('/',mainpage)],debug=True)