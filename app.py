from __future__ import print_function
from flask_restful import Resource
from flask_restful import Api
from flask import send_file
from flask import request
from flask import Flask
from json import dumps
from flask import jsonify
from flask_cors import CORS
import json 
import random
import os
import os.path
import sys
from io import BytesIO

from OCC.STEPControl import STEPControl_Reader
from OCC.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.WebGl import threejs_renderer
from OCC.Visualization import Tesselator


def read_step_file(filename):
    """ read the STEP file and returns a compound
    """
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:  # check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        aResShape = step_reader.Shape(1)
    else:
        print("Error: can't read file.")
        sys.exit(0)
    return aResShape

def import_as_one_shape(event=None):
    shp = read_step_file(os.path.join('.', 'LampExample.step'))
    tess = Tesselator(shp)
    tess.Compute()
    threejsString = tess.ExportShapeToThreejsJSONString('someid')
    # with open("outputs/threejs/shape.json", "w") as f: 
    #    f.write(threejsString)
    return threejsString

def import_as_compound(event=None):
    compound = read_step_file(os.path.join('.', 'models', 'as1_pe_203.stp'))
    t = Topo(compound)
    display.EraseAll()
    for solid in t.solids():
        color = Quantity_Color(random.random(),
                               random.random(),
                               random.random(),
                               Quantity_TOC_RGB)

app = Flask(__name__)
api = Api(app)
CORS(app)

class step(Resource):
    def get(self):
        strIO = BytesIO()
        jsonStr = import_as_one_shape()
        strIO.write(jsonStr.encode())
        strIO.seek(0)
        return send_file(strIO, attachment_filename="testing.json", as_attachment=True)

    def post(self):
        print(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file)
            return 'You posted a file'

class home(Resource):
    def get(self):
        return 'This is Smelter'

api.add_resource(home, '/smelt')
api.add_resource(step, '/smelt/step')


if __name__ == '__main__':
     app.run()
