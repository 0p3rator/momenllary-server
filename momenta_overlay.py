#!flask/bin/python
from flask import Flask, jsonify, request, Response, redirect
from flask import abort
import psycopg2
from jsonifyimage import jsonify_image
from mycolorlog import UseStyle
from sign_s3url import create_presigned_url
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
    return redirect('https://www.baidu.com')
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
    
@app.route('/images/')
@app.route('/images')
def get_images():   
    print UseStyle('red',   fore = 'red')
    params = request.args
    bbox = params.get('bbox').split(',')
    FeatureCollection = jsonify_image(bbox) 
    jsonResp = json.dumps(FeatureCollection) 
    js = json.dumps({'task':'taskliulwx'})
    resp = Response(jsonResp, status=200,mimetype='application/json')
    resp.headers['Link'] = 'http://I.Want.you.com'
    return resp

@app.route('/imagekey/')
def get_image_key():
    print UseStyle('Image_Key',   fore = 'red')
    params = request.args
    image_key = params.get('imagekey')
    print image_key
    image_key = 'map-data/' + image_key
    print UseStyle(image_key, fore = 'blue')
    url = create_presigned_url('momenta-hdmap',image_key)
    print UseStyle(url, fore = 'red')
    return redirect(url)
    return json.dumps({'url': url})

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_task():
    return jsonify({'tasks': tasks})   
   

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Expose-Headers','Link')
    return response


if __name__ == '__main__':
    app.run(debug=True)
