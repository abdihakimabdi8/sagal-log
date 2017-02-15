
import os
import webapp2
import jinja2
import cgi
import re
from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
def code(lineHaul, fuelAdvance):
    brokerCommission = lineHaul*(float(.10))
    netOfCommision = lineHaul -int(brokerCommission)
    netHaul = netOfCommision - fuelAdvance
    return netHaul
def netPayForm(netpay):
    netPay = "<div id='net'> Net Pay<form action='/load' method='post'><textarea>"+ netpay +"</textarea></form></div>"
    return netPay
class Index(Handler):
    def get(self):
        t = jinja_env.get_template("signup-form.html")
        content = t.render(error=self.request.get("error"))
        self.response.write (content)
class SignUp(Handler):
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirm_password = self.request.get("confirm")
        email =self.request.get("email")
        have_error = False
        params = dict(username = username,
                      email = email)
        if not valid_username(username):
            params['error_username'] = " Please provide valid username"
            have_error = True

        if not valid_password(password):
            params['error_password'] = " Please provide valid password"
            have_error = True

        if (confirm_password == password)==False:
            params['error_verify'] = "Password Verification failed"
            have_error = True
        if not valid_email(email):
            params['error_verify'] = " Please provide valid E-mail"
            have_error = True
        if have_error:
            self.render('signup-form.html', **params)
        else:

            self.redirect('/welcome?username=' + username)
class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')
class NewLoad(Handler):
    def get(self):
            self.render( 'load-form.html')
    def post(self):
        owner_operator = self.request.get('owner')
        loadNumber = self.request.get('loadnumber')
        description = self.request.get('description')
        lineHaul = int(self.request.get("lineHaul"))
        fuelAdvance = int(self.request.get("fuelAdvance"))
        net_pay = code(lineHaul, fuelAdvance)
        contentTwo = netPayForm(str(net_pay))
        #self.render( 'load-form.html', net_pay=net_pay)
        if owner_operator and loadNumber and description and lineHaul and fuelAdvance and net_pay:
            l = Load(parent = blog_key(), owner_operator = owner_operator, loadNumber = loadNumber, description = description, lineHaul=lineHaul, fuelAdvance=fuelAdvance, net_pay=net_pay)
            l.put()
            self.redirect('/netpay/%s' % str(l.key().id()))
        else:
            error = "submit valid Load info, please!"
            self.render("load-form.html", owner_operator = owner_operator, loadNumber = loadNumber, description = description, lineHaul=lineHaul, fuelAdvance=fuelAdvance, error=error)
def blog_key(name = 'default'):
    return db.Key.from_path('load', name)

class Load(db.Model):
    owner_operator = db.StringProperty(required = True)
    loadNumber = db.StringProperty(required = True)
    description = db.StringProperty(required = True)
    lineHaul= db.IntegerProperty(required=True)
    fuelAdvance = db.IntegerProperty(required=True)
    net_pay = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.net_pay
        return render_str("load.html", l = self)
class NetPay(Handler):
    def get(self):
        loads = db.GqlQuery("select * from Load order by created desc limit 3")
        self.render('load-table.html', loads = loads)
class LoadPage(Handler):
    def get(self, load_id):
        key = db.Key.from_path('Load', int(load_id), parent=blog_key())
        load = db.get(key)

        if not load:
            self.error(404)
            return

        self.render("permalink.html", load = load)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', SignUp),
    ('/welcome', Welcome),
    ('/load', NewLoad),
    ('/netpay/?', NetPay),
    ('/netpay/([0-9]+)', LoadPage),
], debug=True)
