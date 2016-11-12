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

    error = None
    metadata = request.form['metadata']
    image = request.form['image']

    #primavera_output = primavera({...})
    return {primavera_output}
