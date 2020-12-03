import mysql.connector
from datetime import datetime
from flask import Flask
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="123",
database="test"
)

app = Flask(__name__)

@app.route("/")
def index():
    mycursor = mydb.cursor()
    print("Connected..")
    sql = "SELECT * FROM test2"
    mycursor.execute(sql)
    output = mycursor.fetchall()
    return str(output)

    
    
