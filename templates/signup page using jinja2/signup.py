import webapp2
import os
import jinja2
import re
template_dir=os.path.dirname(__file__)
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_un(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_pass(password):
	return PASS_RE.match(password)

EMAIL_RE=re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

class handler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)
	def render_str(self,template,**params):
		t=jinja_env.get_template(template)
		return t.render(params)
	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))

class welcome(handler):
	def get(self):
		m=self.request.get('username')
		self.render('welcomehtml.html',g=m)

class mainpage(handler):
	def get(self):
		self.redirect("/signup")

class ConverterPage(handler):
	def get(self):
		y=""
		text=self.request.get("form_input")
		if text:
			y=text.encode('rot13')
		self.render("gurjothtml.html",n=y)

class SignupPage(handler):
	def get(self):
		self.render("signuphtml.html")
	def post(self):
		username=self.request.get('usernameInput')
		password=self.request.get('passwordInput')
		verify=self.request.get('verifyPasswordInput')
		email=self.request.get('emailInput')
		
		u_error=""
		p_error=""
		v_error=""
		email_error=""
		if username:
			if(valid_un(username)):
				u_error=""
			else:
			 	u_error="username must be 3 to 20 characters long"
		else:
			u_error="this field cannot be left blank"

		if password:
			if(verify!=password):
				v_error="! passwords dont match"
				verify=""
			if(valid_pass(password)):
				p_error=""
			else:
				p_error="password need to be 3 to 20  character long"
		else:
			p_error="this field cannot be left blank"
		
		if email:
			if(valid_email(email)):
				email_error=""
			else:
				email_error="invalid email address"
		if(u_error=="" and p_error=="" and v_error=="" and email_error==""):
			self.redirect("/welcome/?username="+username)
		else:
			self.render("signuphtml.html",usernameInput=username,passwordInput=password,verifyPasswordInput=verify,emailInput=email,usernameError=u_error,passwordError=p_error,verifyError=v_error,emailError=email_error)

app=webapp2.WSGIApplication([('/',mainpage),('/rot13',ConverterPage),('/signup',SignupPage),('/welcome/',welcome)],debug=True)
