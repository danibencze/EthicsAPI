from flask import Flask, session, redirect, url_for, escape, request, jsonify
from ldap3 import Server, Connection, ALL
import pymysql.cursors

app = Flask(__name__)


# whenever someone wants to access the database call this function first
def databaseConnection():
	connection = pymysql.connect(host='csmysql.cs.cf.ac.uk',
	                             user='group12.2017',
	                             password='rwqeBE4DBj5vdk',
	                             db='group12_2017',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def checkpermission(userName):
	if 'username' in session:
		connection = databaseConnection()
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * FROM Admins WHERE uName=%s "
				cursor.execute(sql, userName)
				result = len(cursor.fetchall())
				if result > 0:
					session["admin"] = 1
		finally:
			connection.close()


# main
@app.route('/')
def index():
	if 'username' in session:
		return 'Logged in'
	else:
		return 'You can log in at /auth sending your password and username'


# auth
@app.route('/auth/login', methods=['POST'])
def auth():
	username = request.form['username']
	password = request.form['password']

	srv = Server('ldap.cs.cf.ac.uk', get_info=ALL, use_ssl=True)
	conn = Connection(srv)

	if not conn.bind():
		return "Unable to connect"

	conn.search('ou=people,dc=cs,dc=cardiff.ac.uk', '(uid=USERNAME)')

	# Results will be in conn.entries

	# To authenticate a user who is in LDAP
	# The USER_DN is found in the conn.entries yours would be uid=c1640644,ou=people,dc=cs,dc=cardiff.ac.uk as an example

	srv = Server('ldap.cs.cf.ac.uk', get_info=ALL, use_ssl=True)
	conn = Connection(srv, user='uid=' + username + ',ou=people,dc=cs,dc=cardiff.ac.uk', password=password)
	if conn.bind():
		session["username"] = username
		checkpermission(username)
		if 'admin' in session:
			return "You have logged in as an admin"
		else:
			return "Successful login"
	else:
		return "Incorrect credentials"


@app.route('/auth/logout')
def logout():
	session.pop('username', None)
	session.pop('admin', None)
	return redirect(url_for('index'))


# view applications
@app.route('/applications/all')
def viewApplication():
	if 'username' in session:
		connection = databaseConnection()
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * FROM General"
				cursor.execute(sql)
				result = cursor.fetchall()
		finally:
			connection.close()
			return jsonify(result)
	else:
		return "You need to login to view this resource"


@app.route('/applications/<variable>')
def viewById(variable):
	if 'username' in session:
		connection = databaseConnection()
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * FROM General WHERE ID =" + variable
				cursor.execute(sql)
				result = cursor.fetchall()
		finally:
			connection.close()
			return jsonify(result)
	else:
		return "You need to login to view this resource"


# Fix this Matt
# submit application
@app.route('/applications/submit', methods=["POST"])
def submitApplication():
	if 'username' in session:
		connection = databaseConnection()
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO 'Info' ('stu_no', 'stu_name', 'app_status') VALUES (%s, %s, %s)"
				cursor.execute(sql, (request.form['stu_no'], request.form["stu_name"], request.form["app_status"]))
				connection.commit()
		finally:
			connection.close()
			return "Application successfully submitted."
	else:
		return "You need to login to view this resource"

@app.route('/admins/addnew', methods=['POST'])
def addNewAdmin():
	if 'admin' in session:
		connection = databaseConnection()
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO 'Admins'('uName') VALUES (%s)"
				cursor.execute(sql, (request.form["uName"]))
				connection.commit()
		finally:
			connection.close()
		return result
		# Access the admins table
		# Create a new entry
		# POST variables: uName
		# request.form["uName"]
		#v1
	else:
		return 'Access denied'


app.secret_key = '\xe9]\x19c\x98\x10\xf0q\xc1\x18\x18|A/\xdd\xd3\x8fM\t\xa4\x18\xd1d\xf3{vL\xb0\xbe\xbd'

if __name__ == "__main__":
	app.run(host='0.0.0.0')

# another database with all the admin names in it.
# Whenever an admin is added to the admins table trigger another insert to the voting table

# Make a
