# -*- coding: utf-8 -*-  
from flask import Flask, render_template, Response
from vidgear.gears import NetGear
from imutils import build_montages
import cv2
import time
import logging
logging.basicConfig(filename="/var/log/tb_camera.log",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#activate multiserver_mode
options = {'multiserver_mode': False}

#Change the Client with your system IP address and port address of each unique Server((5566,5567) in our case), plus activate pattern Request/Reply(`1`), `recieve_mode`, and `logging` for debugging
#client = NetGear(address = "10.1.47.23", port = "5566", protocol = 'tcp', pattern = 1, logging=True, receive_mode = True, **options)

camstream = []
camstream_cap = []

class CamStreamer(object):
    def __init__(self):
        self.client = NetGear(address = "192.168.0.10", port = "5567", protocol = 'tcp', pattern = 1, logging=True, receive_mode = True, **options)

    def __del__(self):
        self.client.close()

    def get_frame(self):
        frame = None
        try:
            image = self.client.recv()
            # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            #print frame
        except:
            #print "frame process error!"
            if camstream:
                cam = camstream.pop()
                del cam
        return frame

app = Flask(__name__)

@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')

def gen(camera):
    while True:
        time.sleep(0.01)
        frame = camera.get_frame()
        if not frame:
            break
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    if not camstream:
        camStr = CamStreamer()
        camstream.append(camStr)
    return Response(gen(camstream[0]),
                    mimetype='multipart/x-mixed-replace;boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=15001)
