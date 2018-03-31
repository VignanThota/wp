from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'
data = SQLAlchemy(app)

class Users(data.Model):
	__tablename__='user_accounts'
	email = data.Column(data.String(255),primary_key=True)
	password = data.Column(data.String(255))
	def __init__(self,email,password):
		self.email=email
		self.password=password
data.create_all()

@app.route('/')
def access():
	return render_template('index.html')
@app.route("/register",methods = ['GET','POST'])
def register():
	print("hello")
	if request.method =='POST':
		password = request.form['password']
		cpassword = request.form['cpassword']
		email = request.form['email']
		if str(password)==str(cpassword):
			user = Users(email,password)
			data.session.add(user)
			data.session.commit() 
			return render_template('index.html',error='Registration Success')
		else:
			return render_template('index.html',error='password mismatch')
		
if __name__=='__main__':
	app.run(host="127.0.0.1", port=int("8033"),debug=True)