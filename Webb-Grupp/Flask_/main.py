from flask import Flask, session, request, render_template, redirect, flash, g, url_for 

from db import get_db

import werkzeug
from werkzeug.security import (
    check_password_hash, generate_password_hash
)

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = "BAJS"

@app.route("/", methods=("GET", "POST")) 
def index():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		
		db = get_db()
		r = db.cursor()
		r.execute("SELECT * FROM users")
		r = r.fetchall()

		for account in r:
			if account[1] == username:
				if check_password_hash(account[2], password):
					#Användaren HAR loggat in..
					session['logged'] = True
					return redirect(url_for('logged'))
				else:
					return "Lösenord incorrect"
		
		return "Inga konton hittades"

	session.clear()
	return render_template('index.html', user="Harry")

@app.route("/register", methods=("GET", "POST")) 
def create():
	if request.method == "POST":
		cusername = request.form['create_username']
		cpassword = request.form['create_password']
		repassword = request.form['create_re-password']
		email = request.form['email']

		db = get_db()
		r = db.cursor()
		user_exists = r.execute("SELECT * FROM users WHERE username=%s", (cusername))
		email_exists = r.execute("SELECT * FROM users WHERE email=%s", (email))

		if user_exists > 0:
			return "Användarnamnet används redan"
		
		elif cpassword != repassword:
			return "Lösenorden matchar inte"

		elif email_exists > 0:
			return "Emailen används redan"
		else:
			r = db.cursor()
			r.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s) ", (cusername, generate_password_hash(cpassword), email))
			db.commit()


	session.clear()
	return render_template('index.html')

@app.route("/login", methods=('GET', 'POST'))


@app.route("/logged")
def logged():

	if session.get('logged'):
		return "Du är inloggad"
	else:
		return "Du är INTE inloggad"
		
if __name__ == "__main__":
	app.run(debug=True)
	