import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="@Nielong080848",
)
my_cursor = mydb.cursor()

my_cursor.execute("")
