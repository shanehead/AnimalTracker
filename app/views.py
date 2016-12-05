from app import app, api_manager
from flask import request, Response
from models import api_models
from tools import s3_upload
import json

# Create API endpoints
for model_name in api_models:
    model_class = api_models[model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'], allow_patch_many=True)

@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')

@app.route('/add_animal', methods=['POST'])
def add_animal():
    upload_file = request.files['file']
    print "method=add_animal upload_file='%s'" % str(upload_file)
    if upload_file:
        photo_uri = s3_upload(upload_file)
        data = {'photo_uri': photo_uri}
        resp = Response(json.dumps(data), status=200, mimetype='application/json')
        return resp
