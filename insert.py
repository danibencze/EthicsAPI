import pymysql.cursors

connection = pymysql.connect(host='csmysql.cs.cf.ac.uk',
                             user='user',
                             password='pwd',
                             db='group12_2017',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
	with connection.cursor() as cursor:
		sql = "INSERT INTO General (Title) VALUES (%s)"
		cursor.execute(sql, "Asd")
		result = cursor.fetchall()
		print(result)
finally:
	connection.close()
