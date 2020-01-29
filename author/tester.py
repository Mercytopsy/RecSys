import mysql.connector

def execute():
    mydb = mysql.connector.connect(
    host="localhost",
    user="Dietitian_app",
    passwd="diet_password",
    database="Dietitians"
)
    mycursor = mydb.cursor()
    return mycursor
 
