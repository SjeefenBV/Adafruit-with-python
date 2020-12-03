import pyfirmata
import time
from Adafruit_IO import Client, Feed, RequestError
import mysql.connector
from datetime import datetime
from threading import Thread

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="xxx",
database="test"
)

board = pyfirmata.Arduino("/dev/ttyACM0")
digital_output = board.get_pin("d:13:o")
analog_input = board.get_pin("a:0:i")

ADAFRUIT_IO_USERNAME = "Sjeefen"
ADAFRUIT_IO_KEY = "aio_uFgR74nptWJDPmdVgBVxU8T8ci2f"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

it = pyfirmata.util.Iterator(board)
it.start()
print("Running...")

state = "1"

def mysql():
    while True:
        if aio.receive('welcome-feed').value == "ON":
            state = "2"
        else:
            state = "1"
        mycursor = mydb.cursor()
        sql1 = "TRUNCATE TABLE test2"
        mycursor.execute(sql1)
        print("Connected..")
        sql2 = "INSERT INTO test2(id,name) VALUES (%s,%s)"
        val = (state, datetime.now())
        mycursor.execute(sql2, val)
        mydb.commit()
        time.sleep(2)

def adafruiit():
        run_count = 1
        print("Counting: ", run_count)
        run_count += 1
        aio.send_data("counter", run_count)
    
        print("Potentiometer Value: ", analog_input.read())
        aio.send_data("pot", analog_input.read())
        
        data = aio.receive('welcome-feed')
    
        print("Data:", data.value)
    
        if data.value == "ON":
            digital_output.write(True)
        else:
            digital_output.write(False)
        
        time.sleep(2)
    
print(aio.receive('welcome-feed').value)
t1 = Thread(target=mysql)
t2 = Thread(target=adafruiit())

try:
    digital = aio.feeds("digital")
except RequestError:
        feed = Feed(name = "digital")
        digital = aio.create_feed(feed)

t1.start()
t2.start()
while True:
    t1.join()
    t2.join()
