#!flask/bin/python
# -*- coding: UTF-8 -*- 
from flask import Flask, jsonify, request, Response, redirect, url_for
from flask import abort
import psycopg2
from mycolorlog import UseStyle
from service.image_service import ImageService
from service.detection_service import DetectionService
from service.check_service import CheckService
import json
import re
import time as time

conn = None

app = Flask(__name__)

@app.before_request
def before_request():
    print UseStyle(request.method, fore = 'red')
    print request.endpoint

@app.route('/')
def index():
    js = json.dumps({'task':'taskliulwx'})
    txt = file('static/SPf5iPZ_rC5n9WJBGAbF2Q')
    resp = Response(txt, status=200, mimetype='application/json')
    return resp

@app.route('/sequences/')
def hello1():
    params = request.args
    # bbox = params.get('bbox').split(',')
    # FeatureCollection = jsonify_image(bbox) 
    result = {'test':1} 
    return Response(json.dumps(result), status = 200,mimetype='application/json')
    
#@app.route('/images/')
@app.route('/images')
def get_images():  

    starttime = time.clock()
    requestUrl = re.search('\'.*\'', str(request), re.M|re.I).group(0)
    requestUrl = re.sub('\'', '', requestUrl)

    params = request.args
    startkey = params.get('start_key')
    if startkey is not None:
        requestUrl = re.sub('&start_key=[0-9]+', '', requestUrl)

    bbox = params.get('bbox').split(',')
    print UseStyle(bbox, fore = 'yellow')
    imageservice = ImageService()
    FeatureCollection = imageservice.get_images(params, bbox) 

    link = '<{}>; rel="first",'.format(requestUrl)
    if (FeatureCollection['next_start_key'] != 0):
        link = """{}<{}&start_key={}>; rel="next" """.format(link, requestUrl, FeatureCollection['next_start_key'])
    del FeatureCollection['next_start_key']

    length = len(FeatureCollection['features'])
    print UseStyle(length, fore = 'yellow')
    jsonResp = json.dumps(FeatureCollection) 
    resp = Response(jsonResp, status=200,mimetype='application/json')
    resp.headers['Link'] = link

    endtime = time.clock()
    print UseStyle(('Total Time cost:', endtime - starttime), fore = 'yellow')
    return resp

#@app.route('/imagekey/')
@app.route('/imagekey')
def get_image_key():
    print UseStyle('Image_Key',   fore = 'red')
    params = request.args
    detectionService = DetectionService()
    url = detectionService.get_s3url(params)
    print UseStyle(url, fore = 'red')
    return redirect(url)
  

@app.route('/object')
def get_objects():
    params = request.args
    bbox = params.get('bbox').split(',')
    object_service.get_objects(bbox)
    print UseStyle(bbox, fore = 'red')
    return jsonify({'tasks': tasks})  

#@app.route('/detection/')
@app.route('/detection', methods=['GET'])
def get_detections():
    starttime = time.time()
    params = request.args
    detectionService = DetectionService()
    url = detectionService.get_s3url(params)
    return redirect(url)


@app.route('/location/keyframe', methods=['GET','POST'])
def get_frame_location():
    imageKey = request.values.get('imagekey')
    print imageKey
    detectionService = DetectionService() 
    result = detectionService.get_frame_location(imageKey)
    return Response(json.dumps(result), status = 200,mimetype='application/json')

@app.route('/location/packet', methods=['GET', 'POST'])
def get_packet_location():
    packetName = request.values.get('packetname')
    print packetName
    detectionService = DetectionService()
    result = detectionService.get_packet_location(packetName)
    return Response(json.dumps(result), status = 200, mimetype = 'application/json')

@app.route('/checkresult',methods=['GET', 'POST'])
def record_check_result():
    checkService = CheckService()
    result = checkService.upload_check_result(request)
    return Response(json.dumps(result), status = 200, mimetype = 'application/json')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Expose-Headers','link')
    return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0' ,port = 5123, debug=True)
