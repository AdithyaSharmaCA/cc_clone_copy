import mysql.connector

# Print out connection parameters for debugging
print("Connecting to MySQL database with host='mysql', user='root', password='Adithya@123', database='cc_project'")
try:
    cnx = mysql.connector.connect(user='root', password='Adithya@123',
                                  host='mysql', database='cc_project')
    print("Connection successful!")
except mysql.connector.Error as err:
    print("Error:", err)
