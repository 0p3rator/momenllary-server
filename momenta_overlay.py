#!flask/bin/python
# -*- coding: UTF-8 -*- 
from flask import Flask, jsonify, request, Response, redirect, url_for
from flask import abort
from mycolorlog import UseStyle
from service.image_service import ImageService
from service.detection_service import DetectionService
from service.check_service import CheckService
from service.sequence_service import SequenceService
from login import login_router
import json
import re
import time as time
import os 
from flask_caching import Cache
import urllib

app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE':'filesystem',
    'CACHE_DIR': './flask_cache',
    'CACHE_DEFAULT_TIMEOUT': 360000,
    'CACHE_THRESHOLD': 2048
})
# app.register_blue#print(login_router)

@app.before_request
def before_request():
    print(UseStyle(request.method, fore = 'red'))
    print(request.endpoint)

@app.route('/')
def index():
    js = json.dumps({'task':'taskliulwx'})
    txt = file('static/SPf5iPZ_rC5n9WJBGAbF2Q')
    resp = Response(txt, status=200, mimetype='application/json')
    return resp

def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key

@app.route('/sequences', methods=['GET'])
# @cache.cached(key_prefix=cache_key)
def get_sequence():
    
    requestUrl = re.search('\'.*\'', str(request), re.M|re.I).group(0)
    requestUrl = re.sub('\'', '', requestUrl)

    params = request.args
    startkey = params.get('start_key')
    if startkey is not None:
        requestUrl = re.sub('&start_key=[0-9]+', '', requestUrl)

    sequence_service = SequenceService()
    features_collection = sequence_service.get_sequences(params) 

    link = '<{}>; rel="first",'.format(requestUrl)
    if (features_collection['next_start_key'] != 0):
        link = """{}<{}&start_key={}>; rel="next" """.format(link, requestUrl, features_collection['next_start_key'])
    del features_collection['next_start_key']
    # return Response('{"hello": "test"}', status=200, mimetype='application/json')
    resp = Response(json.dumps(features_collection), status = 200,mimetype='application/json')
    resp.headers['Link'] = link
    return resp
    
@app.route('/images')
@cache.cached(key_prefix=cache_key)
def get_images():  
    starttime = time.clock()
    requestUrl = re.search('\'.*\'', str(request), re.M|re.I).group(0)
    requestUrl = re.sub('\'', '', requestUrl)

    params = request.args
    startkey = params.get('start_key')
    if startkey is not None:
        requestUrl = re.sub('&start_key=[0-9]+', '', requestUrl)

    bbox = params.get('bbox').split(',')
    #print(UseStyle(bbox, fore = 'yellow'))
    imageservice = ImageService()
    FeatureCollection = imageservice.get_images(params, bbox) 

    link = '<{}>; rel="first",'.format(requestUrl)
    if (FeatureCollection['next_start_key'] != 0):
        link = """{}<{}&start_key={}>; rel="next" """.format(link, requestUrl, FeatureCollection['next_start_key'])
    del FeatureCollection['next_start_key']

    length = len(FeatureCollection['features'])
    #print(UseStyle(length, fore = 'yellow'))
    jsonResp = json.dumps(FeatureCollection) 
    print(UseStyle(("TEST"), fore='yellow'))
    resp = Response(jsonResp, status=200,mimetype='application/json')
    resp.headers['Link'] = link
    endtime = time.clock()
    #print(UseStyle(('Total Time cost:', endtime - starttime), fore = 'yellow'))
    return resp

@app.route('/imagekey')
def get_image_key():
    #print(UseStyle('Image_Key',   fore = 'red'))
    params = request.args
    detectionService = DetectionService()
    url = detectionService.get_s3url(params)
    #print(UseStyle(url, fore = 'red'))
    return redirect(url)
  
@app.route('/object')
def get_objects():
    params = request.args
    bbox = params.get('bbox').split(',')
    # object_service.get_objects(bbox)
    #print(UseStyle(bbox, fore = 'red'))
    return jsonify({'tasks': 'ab'})  

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
    #print(imageKey)
    detectionService = DetectionService() 
    result = detectionService.get_frame_location(imageKey)
    return Response(json.dumps(result), status = 200,mimetype='application/json')

@app.route('/location/packet', methods=['GET', 'POST'])
def get_packet_location():
    packetName = request.values.get('packetname')
    #print(packetName)
    detectionService = DetectionService()
    result = detectionService.get_packet_location(packetName)
    return Response(json.dumps(result), status = 200, mimetype = 'application/json')

@app.route('/checkresult',methods=['POST'])
def record_check_result():
    checkService = CheckService()
    try:
        result = checkService.upload_check_result(request)
        resp = None
        origin = request.environ['HTTP_ORIGIN'] 
        if result['result'] == 'OK':
            resp = Response(json.dumps(result), status = 200, mimetype = 'application/json')
        else:
            resp = Response(json.dumps(result), 401, {'WWWAuthenticate':'Basic realm="Login Required"'})
        resp.headers.add('Access-Control-Allow-Credentials', "true")
        resp.headers.add('Access-Control-Allow-Origin', origin)
        return resp
    except Exception as e:
        #print(e)
        abort(404)

@app.route('/checkresult/<variable>',methods=['POST'])
def get_check_result(variable):
    checkService = CheckService()
    try:
        origin = request.environ['HTTP_ORIGIN']
        result = checkService.get_check_result(variable, request)
        #print(result)
        resp = None
        if result.has_key('result'):
            resp =  Response(json.dumps(result), 401, {'WWWAuthenticate':'Basic realm="Login Required"'})
        else:
            resp = Response(json.dumps(result), status = 200, mimetype = 'application/json')
        resp.headers.add('Access-Control-Allow-Credentials', "true")
        resp.headers.add('Access-Control-Allow-Origin', origin)
        return resp            
    except Exception as e:
        #print(e)
        abort(404)

@app.after_request
def after_request(response):
    if response.headers.get('Access-Control-Allow-Origin') is None:
        response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Expose-Headers','link')
    return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0' ,port = 5123, debug=True)
