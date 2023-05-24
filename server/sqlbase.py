import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Maker",
  password="schillercoin4ever"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")