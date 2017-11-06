from flask_restful import Resource
from flask_restful import Api
from flask import send_file
from flask import request
from flask import Flask
from json import dumps

brd = '/root/code/Smelter/photon.brd'

app = Flask(__name__)
api = Api(app)

class stl(Resource):
    def get(self):
        return {'stl': 'None'}

class eagle(Resource):
    def get(self):
        image = image3d.export_image3d(brd, 'api_3d.png')
        return serve_image(image)

def serve_image(img):
    img_io = StringIO()
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

api.add_resource(stl, '/smelt/stl')
api.add_resource(eagle, '/smelt/eagle')

if __name__ == '__main__':
     app.run()
