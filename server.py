from flask import Flask
from flask import request
from flask import render_template

from primavera.primavera.primavera import primavera

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html");

@app.route("/submit",methods=["POST"])
def run():
    '''takes posts to /submit and runs it through primavera'''

    print(request.form)

    error = None
    image = request.form['image']
    palette = request.form['palette']
    numcolors = request.form['colors']
    overshoot = request.form['overshoot']
    merge = request.form['merge']

    print(image)
    primavera_output = primavera(image=image, colors=palette,
                                 palette_size=numcolors, overshoot=overshoot,
                                 merge=merge)
    return {primavera_output}
