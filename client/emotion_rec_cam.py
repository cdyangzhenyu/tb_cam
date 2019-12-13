from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
from vidgear.gears import NetGear
import time
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("/data/log/tb_cam.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#activate multiserver_mode
options = {'multiserver_mode': False}

#change following IP address '192.168.1.xxx' with Client's IP address and assign unique port address(for e.g 5566).
server = NetGear(address = "your ip", port = '5566', protocol = 'tcp',  pattern = 1, receive_mode = False, logging=True, **options) # and keep rest of settings similar to Client

cur_path = sys.path[0]
# parameters for loading data and images
detection_model_path = cur_path+'/emotion_rec/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = cur_path+'/emotion_rec/models/_mini_XCEPTION.102-0.66.hdf5'
preds=[]
# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised","neutral"]

feelings_faces = []
emoji_face = []
for index, emotion in enumerate(EMOTIONS):
    feelings_faces.append(imutils.resize(cv2.imread(cur_path+'/emotion_rec/emojis/' + emotion + '.png', -1),height=60,width=60))

# starting video streaming
#cv2.namedWindow('your_face')
camera = cv2.VideoCapture(0)
fps_num = 0
current_fps = 0
time_of_all = 0
time_of_calc = 0
time_of_trans = 0
start_time = time.time()
while True:
    new_time = time.time()
    time_of_calc = new_time
    delta = new_time - start_time
    if delta >= 1:
        start_time = new_time
        current_fps = fps_num
        fps_num = 0
    frame = camera.read()[1]
    frame = imutils.resize(frame,width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)

    canvas = np.zeros((250, 300, 3), dtype="uint8")
    frameClone = frame.copy()
    
    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
        # the ROI for classification via the CNN
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]

        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)

                # draw the label + probability bar on the canvas
                emoji_face = feelings_faces[np.argmax(preds)]
                w = int(prob * 300)
                cv2.rectangle(canvas, (7, (i * 35) + 5),
                (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (255, 255, 255), 2)
                cv2.putText(frameClone, label, (fX, fY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                              (0, 0, 255), 2)
        for c in range(0, 3):
            frameClone[10:70, 240:300, c] = emoji_face[:, :, c] * \
            (emoji_face[:, :, 3] / 255.0) + frameClone[10:70,
            240:300, c] * (1.0 - emoji_face[:, :, 3] / 255.0)
    time_of_calc = round((time.time()-time_of_calc), 4)*1000
    cv2.putText(frameClone, "FPS: %sfps" % current_fps, (10, 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 1)
    cv2.putText(frameClone, "ALL_TIME: %sms" % time_of_all, (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 1)
    cv2.putText(frameClone, "CALC_TIME: %sms" % time_of_calc, (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 1)
    cv2.putText(frameClone, "TRANS_TIME: %sms" % time_of_trans, (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0,0,255), 1)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    time_of_trans = time.time()
    try:
        server.send(frameClone)
    except:
        pass
    fps_num = fps_num + 1
    
    #cv2.imshow('your_face', frameClone)
    #cv2.imshow("Probabilities", canvas)
    time_of_trans = round((time.time()-time_of_trans), 4)*1000
    time_of_all = time_of_calc + time_of_trans
    print "time_of_all: %sms, time_of_calc: %sms,time_of_trans: %sms, current_fps: %sfps" % (time_of_all, time_of_calc, time_of_trans, current_fps)
    logger.info("time_of_all: %sms, time_of_calc: %sms,time_of_trans: %sms, current_fps: %sfps" % (time_of_all, time_of_calc, time_of_trans, current_fps))

camera.release()
server.close()
#cv2.destroyAllWindows()
