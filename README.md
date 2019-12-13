# Thingsboard local usb camera demo (IoT)

## This project is just a demo, it's function include:
- Emotion Recognition use local usb camera(has two steering gear) on Respberry PI 4B.
- Use vidgear transmit real-time streaming to thingsboard cloud server.
- Add a thingsboard widget to display the real-time streaming.
- Control the steering gear from cloud manual or automatic (Arduino and zigbee).

## server code
- [Vidgear](https://github.com/abhiTronix/vidgear) is a multi-threaded Video Processing Python framework. The server receive the streaming from the client.
- Cloud server has a flask http service to receive the tcp real-time streaming from Respberry PI on local area network and listening a http port 15000. You can display the vedio stream on http://ip:15000.

## client code
- Client code run on PI 4B in LAN. 
- Emotion Recognition ref [emotion_rec](https://github.com/omar178/Emotion-recognition).
