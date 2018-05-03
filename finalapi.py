from flask import Flask, session, redirect, url_for, escape, request, jsonify
from ldap3 import Server, Connection, ALL
import pymysql.cursors

app = Flask(__name__)


# whenever someone wants to access the database call this function first
def database_connect():
	connection = pymysql.connect(host='csmysql.cs.cf.ac.uk',
	                             user='group12.2017',
	                             password='rwqeBE4DBj5vdk',
	                             db='group12_2017',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def check_permission(userName):
	if 'username' in session:
		connection = database_connect()
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
		check_permission(username)
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
def view_application():
	if 'username' in session:
		connection = database_connect()
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
def view_by_id(variable):
	if 'username' in session:
		connection = database_connect()
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


# This should hopefully work, untested because forms being made by someone else - matt
# submit application
@app.route('/applications/submit', methods=["POST"])
def submit_application():
	if 'username' in session:
		connection = database_connect()
		try:
			with connection.cursor() as cursor:

				sql1 = "INSERT INTO 'General' ('ID', 'Title', 'Pre_ID', 'Student_Name', 'Student_Num', 'Supervisor_Name', 'Principle_Researcher', 'Other_Researchers', 'Project_start', 'Project_end', 'Full_Project_Plan', 'FPP_ID', 'Participant_Info_Form', 'PIF_ID', 'Consent_Form', 'CF_ID', 'External_Funding', 'EF_ID', 'Motivations', 'M_ID') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)"

				sql2 = "INSERT INTO 'Info' ('ID', 'N_1', 'N_1_1', 'N_2', 'N_3', 'N_4', 'N_5', 'N_6', 'N_7', 'E_1', 'N_8', 'N_9', 'N_10', 'N_11', 'N_12', 'E_2', 'N_13', 'N_14', 'E_3', 'E_3_3', 'N_15', 'N_16', 'N_16_16', 'N_17', 'E_4', 'E_4_4', 'N_18', 'E_5', 'N_19', 'N_20', 'E_6', 'N_21', 'E_7', 'E_8', 'E_9') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

				cursor.execute(sql1, (
					request.form['ID'], request.form['Title'], request.form['Pre_ID'], request.form['Student_Name'],
					request.form['Student_Num'], request.form['Supervisor_Name'], request.form['Principle_Researcher'],
					request.form['Other_Researchers'], request.form['Project_start'], request.form['Project_end'],
					request.form['Full_Project_Plan'], request.form['FPP_ID'], request.form['Participant_Info_Form'],
					request.form['PIF_ID'], request.form['Consent_Form'], request.form['CF_ID'],
					request.form['External_Funding'], request.form['EF_ID'], request.form['Motivations'],
					request.form['M_ID']))

				cursor.execute(sql2, (
					request.form['ID'], request.form['N_1'], request.form['N_1_1'], request.form['N_2'],
					request.form['N_3'], request.form['N_4'], request.form['N_5'], request.form['N_6'],
					request.form['N_7'],
					request.form['E_1'], request.form['N_8'], request.form['N_9'], request.form['N_10'],
					request.form['N_11'], request.form['N_12'], request.form['E_2'], request.form['N_13'],
					request.form['N_14'], request.form['E_3'], request.form['E_3_3'], request.form['N_15'],
					request.form['N_16'], request.form['N_16_16'], request.form['N_17'], request.form['E_4'],
					request.form['E_4_4'], request.form['N_18'], request.form['E_5'], request.form['N_19'],
					request.form['N_20'], request.form['E_6'], request.form['N_21'], request.form['E_7'],
					request.form['E_8'], request.form['E_9']))

				connection.commit()
		finally:
			connection.close()
			return "Application successfully submitted."
	else:
		return "You need to login to view this resource"


@app.route('/admins/addnew', methods=['POST'])
def add_new_admin():
	if 'admin' in session:
		connection = database_connect()
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO 'Admins'('uName') VALUES (%s)"
				cursor.execute(sql, (request.form["uName"]))
				connection.commit()
		finally:
			connection.close()
		return 'Admin added successfully '
	# Access the admins table
	# Create a new entry
	# POST variables: uName
	# request.form["uName"]
	# v1
	else:
		return 'Access denied'


app.secret_key = '\xe9]\x19c\x98\x10\xf0q\xc1\x18\x18|A/\xdd\xd3\x8fM\t\xa4\x18\xd1d\xf3{vL\xb0\xbe\xbd'

if __name__ == "__main__":
	app.run(host='0.0.0.0')

# another database with all the admin names in it.
# Whenever an admin is added to the admins table trigger another insert to the voting table

# Make a
