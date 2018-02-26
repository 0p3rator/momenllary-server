#!flask/bin/python
from flask import Flask, jsonify, request, Response, redirect
from flask import abort
import psycopg2
from jsonifyimage import jsonify_image
from jsonifyimage import get_path
from mycolorlog import UseStyle
from sign_s3url import create_presigned_url
import service.object_service as object_service
import json

conn = None

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.before_request
def before_request():
    print UseStyle(request.method, fore = 'red')
    print request.endpoint

@app.route('/')
def index():
    js = json.dumps({'task':'taskliulwx'})
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['link'] = 'http://luisrei.com'
    #params = request.args.items()
    #return params.__str__()
    return resp

@app.route('/sequences/')
def hello1():
    params = request.args
    bbox = params.get('bbox').split(',')
    FeatureCollection = jsonify_image(bbox)  

    return jsonify(FeatureCollection)
    
#@app.route('/images/')
@app.route('/images')
def get_images():   
    params = request.args
    bbox = params.get('bbox').split(',')
    FeatureCollection = jsonify_image(bbox) 
    jsonResp = json.dumps(FeatureCollection) 
    js = json.dumps({'task':'taskliulwx'})
    resp = Response(jsonResp, status=200,mimetype='application/json')
    resp.headers['Link'] = 'http://I.Want.you.com'
    return resp

#@app.route('/imagekey/')
@app.route('/imagekey')
def get_image_key():
    print UseStyle('Image_Key',   fore = 'red')
    params = request.args
    imagekey = params.get('imagekey')
    imagePath = get_path(imagekey)
    print imagePath

    imagePath = 'map-data/' + imagePath
    print UseStyle(imagePath, fore = 'blue')
    url = create_presigned_url('momenta-hdmap',imagePath)
    print UseStyle(url, fore = 'red')
    return redirect(url)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_task():
    return jsonify({'tasks': tasks})   

@app.route('/object/')
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
    params = request.args
    imageKey = params.get('imagekey')
    tagType = params.get('tag')
    jsonPath = get_path(imageKey)
    jsonPath = jsonPath.replace('/images','/' + tagType)
    #jsonPath = jsonPath.replace('/images','/json_lane')
    jsonPath = jsonPath.replace('.jpg','.json')
    jsonPath = 'map-data/' + jsonPath
    url = create_presigned_url('momenta-hdmap',jsonPath)
    print UseStyle(url, fore = 'red')
    return redirect(url)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Expose-Headers','Link')
    return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0' ,port = 5123, debug=True)
