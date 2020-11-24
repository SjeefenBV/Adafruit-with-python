import pyfirmata
import time
from Adafruit_IO import Client, Feed, RequestError

run_count = 1
ADAFRUIT_IO_USERNAME = "Sjeefen"
ADAFRUIT_IO_KEY = "aio_nvdT30ogm9qP7iB3lwpFSAUGOBAW"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
board = pyfirmata.Arduino("/dev/ttyACM0")

it = pyfirmata.util.Iterator(board)
it.start()
print("Running...")

digital_output = board.get_pin("d:13:o")
analog_input = board.get_pin("a:0:i")

try:
    digital = aio.feeds("digital")
except RequestError:
        feed = Feed(name = "digital")
        digital = aio.create_feed(feed)
        
while True:
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
    
