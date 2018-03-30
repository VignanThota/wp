from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    password = db.Column(db.String(255))
    email = db.Column(db.String(255),primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    state = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __init__(self,password,email,name,address,state,phone):
        self.password=password
        self.email=email
        self.name=name
        self.address=address
        self.state=state
        self.phone=phone
db.create_all()


@app.route("/")
def index():
	return render_template('login.html',error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('show_books'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('registrationForm'))

def is_valid(email,password):
    stmt = "SELECT email, password FROM users"
    data = db.engine.execute(stmt).fetchall()
    for row in data:
        if row[0] == email and row[1] == password:
            return True
    return False


@app.route("/register",methods = ['GET','POST'])
def register():
    if request.method =='POST':
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        address = request.form['address']
        state = request.form['state']
        phone = request.form['phone']
        user=Users(password,email,name,address,state,phone)
        db.session.add(user)
        db.session.commit()          
        msg="Registered successfully"
        
    db.session.close()
    return render_template("login.html",msg=msg)

@app.route("/registrationForm")
def registrationForm():
    return render_template("register.html")

@app.route('/show_books')
def show_books():
    return render_template('home.html', )
@app.route('/viewcart')
def viewcart():
    return render_template('cart.html')
@app.route("/cart/<tsum>/<int:ni>")
def cart(tsum,ni):
    stmt = "select email,name from users where email='"+session['email']+"'"
    tmt = "select email,phone from users where email='"+session['email']+"'"
    mt = "select email,address from users where email='"+session['email']+"'"
    t = "select email,state from users where email='"+session['email']+"'"
    email, name = db.engine.execute(stmt).fetchone()
    email, phone = db.engine.execute(tmt).fetchone()
    email, address = db.engine.execute(mt).fetchone()
    email, state = db.engine.execute(t).fetchone()
    return render_template("cart.html",email=email,name=name,phone=phone,address=address,state=state,tsum=tsum,ni=ni)
@app.route('/checkout')
def checkout():
    return render_template('CheckOut.html',)    
if __name__ =='__main__':
    
    app.run(debug=True,port=8080)


