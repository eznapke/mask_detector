from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import dash_html_components as html
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import os
from flask import request
import dash
import dash_core_components as dcc
from threading import Thread
import threading
import argparse
import datetime
import imutils
import time
import cv2
import copy
import logging
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

from flask import Flask, Response
import cv2


Address        = "0.0.0.0"
Camera         = None
CameraRun      = True
Frame          = None
WebRawFrame    = None
WebDetectFrame = None
CameraThread   = None
GenRawJPEGThread = None
GenDetectJPEGThread = None

def detect_and_predict_mask(frame, faceNet, maskNet):
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()

        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the detection
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > 0.5:
                        # compute the (x, y)-coordinates of the bounding box for
                        # the object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # ensure the bounding boxes fall within the dimensions of
                        # the frame
                        (startX, startY) = (max(0, startX), max(0, startY))
                        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                        # extract the face ROI, convert it from BGR to RGB channel
                        # ordering, resize it to 224x224, and preprocess it
                        face = frame[startY:endY, startX:endX]
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        face = cv2.resize(face, (224, 224))
                        face = img_to_array(face)
                        face = preprocess_input(face)
                        face = np.expand_dims(face, axis=0)

                        # add the face and bounding boxes to their respective
                        # lists
                        faces.append(face)
                        locs.append((startX, startY, endX, endY))

        # only make a predictions if at least one face was detected
        if len(faces) > 0:
                # for faster inference we'll make batch predictions on *all*
                # faces at the same time rather than one-by-one predictions
                # in the above `for` loop
                preds = maskNet.predict(faces)

        # return a 2-tuple of the face locations and their corresponding
        # locations
        return (locs, preds)


def VideoCamera():
    FPS = 1/30
    FPS_MS = int(FPS * 1000)

    global Frame
    global Camera
    global CameraRun
    global Address

    while CameraRun:
        (status, Frame) = Camera.read()
        time.sleep(FPS)

        if status!=True:

            print("Trying to reconnect to a camera at" + Address)

            capture = cv2.VideoCapture("rtsp://" + Address + ":5554/camy", cv2.CAP_FFMPEG)
            capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
            time.sleep(2)
            if capture.isOpened():
                Camera=capture



def GenerateRawWebFrame():
    while True:
        if str(type(Frame)) == "<class 'NoneType'>":
            time.sleep(2)
            continue

        ret, jpeg = cv2.imencode('.jpg', Frame)
        encodedImage = jpeg.tobytes()
        global WebRawFrame
        WebRawFrame = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'


def GenerateDetectWebFrame():
    while True:

        if str(type(Frame)) == "<class 'NoneType'>":
            time.sleep(2)
            continue

        frame = copy.copy(Frame)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


        ret, jpeg = cv2.imencode('.jpg', frame)
        encodedImage = jpeg.tobytes()
        global WebDetectFrame
        WebDetectFrame = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'


def YealdRawFrame():
    while True:
        #print("Frame")
        yield(WebRawFrame)

def YealdDetectFrame():
    while True:
        yield(WebDetectFrame)


server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.layout = html.Div([html.H1("Webcam Test"), html.Img(src="/raw_video_feed"), html.Img(src="/detect_video_feed")])
#app.layout = html.Div([html.H1("Webcam Test"), html.Img(src="/raw_video_feed")])

@server.route('/raw_video_feed')
def raw_video_feed():
    return Response(YealdRawFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@server.route('/detect_video_feed')
def detect_video_feed():
    return Response(YealdDetectFrame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@server.route('/setcamera/<address>')
def SetCamera(address):

    global Camera
    global Frame
    global CameraRun
    global CameraThread
    global GenRawJPEGThread
    global GenDetectJPEGThread
    global Address

    Address = address

    CameraRun = False

    if CameraThread != None:
        CameraThread.join()


    for i in range(0,5):
        capture = cv2.VideoCapture("rtsp://" + address + ":5554/cam", cv2.CAP_FFMPEG)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        time.sleep(2)
        if capture.isOpened():
            Camera=capture
            break

    if Camera == None:
        return "Unable to add Camera " + address

    CameraRun = True
    CameraThread = Thread(target=VideoCamera, args=())
    CameraThread.daemon = True
    CameraThread.start()

    time.sleep(2)

    if GenRawJPEGThread == None:
        print("Start Raw Thread")
        GenRawJPEGThread = Thread(target=GenerateRawWebFrame, args=())
        GenRawJPEGThread.daemon = True
        GenRawJPEGThread.start()

    #if GenDetectJPEGThread == None:
    #    print("Start Detect Thread")
    #    GenDetectJPEGThread = Thread(target=GenerateDetectWebFrame, args=())
    #    GenDetectJPEGThread.daemon = True
    #    GenDetectJPEGThread.start()

    return "Successfully added Camera at " + address

if __name__ == '__main__':

    CodePath = "/maskdetector/DetectCode/"
    prototxtPath = os.path.sep.join([CodePath, "face_detector", "deploy.prototxt"])
    weightsPath  = os.path.sep.join([CodePath, "face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
    maskNet = load_model(os.path.sep.join([CodePath, "mask_detector.model"]))

    app.run_server(debug=True, port='8080', host='0.0.0.0')
