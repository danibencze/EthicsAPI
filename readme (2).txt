1. Log in

You have to send POST request to http://o0841.cscloud.cf.ac.uk:5000/auth/login this adress with your credentials. 
You can also use the html form provided below.

<form action="http://o0841.cscloud.cf.ac.uk:5000/auth/login" method="post">
<input type="text" name="username">
<input type="password" name="password">
<input type="submit" value="Submit">
</form>

2. I have created an admin database so whenever someone logs in it's being checked automatically if they are in the database or not.
If so an admin session variable is created. 
You can check whether they the logged in user is admin with this statement:

if 'admin' in session:

3. Every resource is log in protected. Make sure that you add the following statement to every endpoint:

if 'username' in session:
	#  They can access the resource
else:
	# Permission denied

4. We have 2 databases for the application and one to store the admins in.

	see the reposrt for the database details
