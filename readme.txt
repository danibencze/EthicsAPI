1. Log in

    You have to send POST request to http://o0841.cscloud.cf.ac.uk:5000/auth/login this adress with your credentials.
    You can also use the html form provided below.

    <form action="http://o0841.cscloud.cf.ac.uk:5000/auth/login" method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="Submit">
    </form>

2. Admins

    I have created an admin database so whenever someone logs in it's being checked automatically if they are in the database or not.
    If so an admin session variable is created.
    You can check whether they the logged in user is admin with this statement:

    if 'admin' in session:

    The session["admin"] variable stores the currently logged in admin's ID.

3. Every resource is log in protected. Make sure that you add the following statement to every endpoint:

    if 'username' in session:
        #  They can access the resource
    else:
        # Permission denied


4. Databases + Voting

	We have two databases to store info about the application. Details in the report.

	One database to store all the details of the admins including their id and email address.

	One voting table. Each record in this database is one vote. Like a voting card.
	Each vote contains either a 1 (Yes) or a 0 (No).
	If you want to check how many admins voted for what just count the votes and group them by appID.


5. Interacting with the database.

    In the user_interfaces folder there are a couple of html files which can be used to demonstrate the functionality.
    What the files are can be used for is in their names.

6. Emails.

    If you want to check how the email sending function is working just put your email and your password in the right variables.
    After that all the emails from your copy will be sent from your email.

7. Additional info

    Please if you push to github make sure that you only push the file you have edited.
    Also make sure that you place it to the right folder.
