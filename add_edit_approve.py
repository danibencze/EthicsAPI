import pymysql

conn = pymysql.connect(host='host', user='user', password='passwd', db='mysqldb')

cur = conn.cursor()

try:
    with cur as cursor:
        # Creates a new record
        sql = "INSERT INTO 'applications' ('stu_no', 'stu_name', 'app_status') VALUES (%s, %s, %s)"
        cursor.execute(sql, ('1619381', 'Liam Hale', 'pending approval'))

    conn.commit()

with cur as cursor:
    # Read a single record
    sql = "SELECT `stu_no`, `stu_name` FROM `applications` WHERE `stu_no`=%s"
    cursor.execute(sql, ('1619381',))
    result = cursor.fetchone()
    print(result)

cur.close()
conn.close()


