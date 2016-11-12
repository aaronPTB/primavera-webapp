from flask import Flask
from flask import request
from flask import render_template
from time import time

from primavera.primavera.primavera import primavera

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html");


palette_locations = {'RGB': 'primavera/rgb.json',
                     'BW': 'primavera/bw.json',
                     'CMYK': 'primavera/cymk.json',
                     'Montana': 'primavera/montana.json'}

@app.route("/submit",methods=["POST"])
def queue_run():
    '''takes posts to /submit and runs it through primavera'''
    if not 'image' in request.files:
        return "needed submit image"

    image = request.files['image']
    palette = palette_locations[request.form['palette']]


    numcolors = int(request.form['colors'])
    dither = request.form['dither']
    if dither == 'None': dither = None

    overshoot = int(request.form['overshoot'])
    merge = None
    if 'merge' in request.form: merge = request.form['merge']

    save_name = str(time())
    file_path = 'primavera/process_queue/'+save_name+'.jpg'
    image.save(file_path)

    print(numcolors, type(numcolors))
    primavera_output = primavera(image=file_path, colors=palette,
                                 palette_size=numcolors, overshoot=overshoot,
                                 merge=merge, dither=dither)

    print(primavera_output)
    return {primavera_output}
