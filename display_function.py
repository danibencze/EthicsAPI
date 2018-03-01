@app.route('/closepoll')
def display(applicationId):

	connection = sqlite3.connect("cardiffdatabase.db")

	cursor = connection.cursor()

	#Check if the currentuser is a committee member
	cursor.execute("SELECT ID FROM committee WHERE ID = currentuser")

	exist = cursor.fetchall()


	#if the user is a committe member then display all
	if exist:

		# we can create an if statement here, to check what is the aplicationid we are currently using here....like if we sort or filtering with date/time
		# or if we are searching on just a name or the application name.... we can add this easily when we create those objects

		cursor.execute("SELECT application_title, submittedby , submittedday FROM applications WHERE application_title LIKE '%' + applicationId + '%' " )
	
		for row in cursor.fetchall():

			#print every row
			print row

			#to be able to get every row and nicely display it in the future interface...should we add them
			#in a txt file?  and retrieve and update that file everytime we start a new query?(this way we can place the 3 components of every row into 3 variables)


	else:

		#explanation, same as above..

		cursor.execute("SELECT application_title, submittedby , submittedday FROM applications where submittedby = currentuser AND ( application_title LIKE '%' + applicationId + '%' ) ")

		for row in cursor.fetchall():

			print row



@app.route('/displayall')
def displayAll(currentuser):

	#two branches one for committe members only they can access it. Although of the current user has some application display them.
	#If committee member display all
	#if(count(SELECT * FROM applications where submiittedby = currentuser) display it as well

	connection = sqlite3.connect("cardiffdatabase.db")

	cursor = connection.cursor()

	#Check if the currentuser is a committee member
	cursor.execute("SELECT ID FROM committee WHERE ID = currentuser")

	exist = cursor.fetchall()


	#if the user is a committe member then display all
	if exist:

		cursor.execute("SELECT application_title, submittedby , submittedday FROM applications")
	
		for row in cursor.fetchall():

			#print every row
			print row

			#to be able to get every row and nicely display it in the future interface...should we add them
			#in a txt file?  and retrieve and update that file everytime we start a new query?(this way we can place the 3 components of every row into 3 variables)


	else:

		cursor.execute("SELECT application_title, submittedby , submittedday FROM applications where submittedby = currentuser")

		for row in cursor.fetchall():

			print row