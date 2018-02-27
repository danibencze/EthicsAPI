from flask import Flask

app = Flask(__name__)
#check session inside every function if not authorised than redirect to auth page
#make an array with all the blocked ip addresses check in every function if the ip is listed or not //not a priority
#workflow: application received >> send an email to the committee members  >> voting takes place >> send an email about the result
#store the Staff id's of the committee members in a database after a successful login if the staff number is in the database than grant permission for everything else
# permission for other users only granted for creating a new application
#in the database there is an isAdmin column if that's 1 than the user can us close() function

#To-Do:
#Artem: Sessions
#Liam: edit/create
#Matt: Workflow diagram/add a committee member
#Ross: Implementing the e-mail sending function
#Rex, Ali: ldap
#Nick: All the displaying functions

@app.route('/')
def hello_world():
	# returns with 1 , only used to test if the server is working
	return 1


#editing applications by id
@app.route('/edit')
def edit(parameter, applicationid, newValue):
	# check permission if the permission is admin ( SELECT * FROM committee where isAdmin NOT NULL) than execute.
	#or if the application is subbmitted by the currently logged in user for eg: if(count(SELECT * FROM applications where userName= $_SESSION["username"])>0) that means true
	return 0

#sumit a new application //used on the applicant side only
@app.route('/create')
def submit(dictionaryWithTheValues):
	return 0

#add a new committee member
@app.route('/addmember')
def submit(dictionaryWithTheUserDetails):
	# check permission if the permission is admin ( SELECT * FROM committee where isAdmin NOT NULL) than execute.
	permission_query = "SELECT * FROM committee WHERE isAdmin NOT NULL"

	insert_query1 = "INSERT INTO committee ("
	insert_query2 = ") VALUES("

	for key in dictionaryWithTheUserDetails:
		insert_query1 += key + ", "
		insert_query2 += dictionaryWithTheUserDetails[key]
		insert_query2 += ", "

	insert_query = insert_query1[:-2] + insert_query2[:-2] + ")"

	#run query

	return 0

#editing committee members
@app.route('/edituser')
def submit(changeThis, toThis, whereUserId):
	return 0

#there is one superior committee member who can accept or reject application any time alone.
@app.route('/closepoll')
def close(applicationId):
	#check permission if the permission is admin ( SELECT * FROM committee where isAdmin NOT NULL) than execute.
	return 0

@app.route('/closepoll')
def display(applicationId):
	return 0

@app.route('/displayall')
def dissplayAll():
	#two branches one for committe members only they can access it. Although of the current user has some application display them.
	#If committee member display all
	#if(count(SELECT * FROM applications where submiittedby = currentuser) display it as well
	return 0

#to is an array
def sendemails(to , title , body):
	#implement the function

def auth(username , passwordhash):
	#ldap auth
	#if successful create a session
	#make a count after 3 tries log the ip address and put it to a array and block it






if __name__ == '__main__':
	app.run()
