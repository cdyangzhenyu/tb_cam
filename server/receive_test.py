from vidgear.gears import NetGear
from imutils import build_montages
import cv2
#activate multiserver_mode
options = {'multiserver_mode': False}

#Change the Client with your system IP address and port address of each unique Server((5566,5567) in our case), plus activate pattern Request/Reply(`1`), `recieve_mode`, and `logging` for debugging
client = NetGear(address = "192.168.0.10", port = "5566", protocol = 'tcp', pattern = 1, logging=True, receive_mode = True, **options) 
#define frame received dict
frame_dict = {}

# infinite loop until [Ctrl+C] is pressed
while True:
	try:
		# receive data
		frame = client.recv()
                print frame
		# check if data received isn't None
		if frame is None:
			break
	except KeyboardInterrupt:
		break

# finally safely close client and release resources
cv2.destroyAllWindows()
client.close()
