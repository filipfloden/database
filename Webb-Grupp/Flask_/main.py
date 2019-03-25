from flask import Flask, session, request, render_template, redirect, flash, g, url_for 

from db import get_db

app = Flask(__name__)
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
				if account[2] == password:
					#Användaren HAR loggat in..
					session['logged'] = True
					return redirect(url_for('logged'))
				else:
					return "Lösenord incorrect"
		
		return "Inga konton hittades"

	session.clear()
	return render_template('index.html')

@app.route("/create", methods=("GET", "POST")) 
def create():
	if request.method == "POST":
		setID = 0
		cusername = request.form['create_username']
		cpassword = request.form['create_password']
		repassword = request.form['create_re-password']
		email = request.form['email']

		db = get_db()
		r = db.cursor()
		r.execute("SELECT * FROM users")
		r = r.fetchall()

		for account in r:
			if account[1] == cusername:
				return "Användarnamnet används redan"
		
			elif cpassword != repassword:
				return "Lösenorden matchar inte"

			else:
				r = db.cursor()
				r.execute("INSERT INTO users (id, username, password, email) VALUES (%s, %s, %s, %s) ", (setID, cusername, repassword, email))
				db.commit()


	session.clear()
	return render_template('index.html')
 
@app.route("/test")
def test():
	db = get_db()
	r = db.cursor()
	r.execute("SELECT * FROM users")
	r = r.fetchall()
	return str(r)
@app.route("/logged")
def logged():

	if session.get('logged'):
		return "Du är inloggad"
	else:
		return "Du är INTE inloggad"
if __name__ == "__main__":
	app.run()
	