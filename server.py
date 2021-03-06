from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from time import time
from base64 import b64encode
import os

from primavera.primavera.primavera import primavera

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html");


palette_locations = {'RGB': 'primavera/primavera/palettes/rgb.json',
                     'BW': 'primavera/primavera/palettes/bw.json',
                     'CMYK': 'primavera/primavera/palettes/cmyk.json',
                     'Montana': 'primavera/primavera/palettes/montana.json'}

@app.route("/submit",methods=["POST"])
def queue_run():
    '''takes posts to /submit and runs it through primavera'''
    if not 'image' in request.files:
        print("document malformed")
        return "needed submit image"

    image = request.files['image']
    palette = palette_locations[request.form['palette']]
    entire = False
    numcolors = int(request.form['colors'])
    dither = request.form['dither']
    overshoot = int(request.form['overshoot'])
    merge = None

    if dither == 'None': dither = None
    if palette != 'primavera/palettes/montana.json': entire = True
    if 'merge' in request.form: merge = request.form['merge']

    save_name = str(time())
    file_path = 'primavera/process_queue/'+save_name+'.jpg'
    image.save(file_path)

    primavera_output = primavera(image=file_path, colors=palette,
                                 palette_size=numcolors, overshoot=overshoot,
                                 merge=merge, dither=dither, entire=entire,
				 save_labels='out')

    with open("out.png", "rb") as output_image:
        img_data = output_image.read()
        data_uri_header = "data:image/png;base64,"
        data_uri_content = b64encode(img_data).decode("utf-8")
        data_uri = data_uri_header + data_uri_content
        os.remove(file_path)
        return jsonify(**{'img': data_uri})

app.run(port=80,host='0.0.0.0')
