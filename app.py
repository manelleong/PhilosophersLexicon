from flask import Flask, render_template, request
import plotly.express as px
import plotly
import json
from services import topic_modeling

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    philosophers = ['confucius', 'nietzsche', 'kant']

    selected_options = [request.form[philosopher] for philosopher in philosophers if request.form.get(philosopher)]

    if not selected_options:
        return render_template('index.html')

    fig = topic_modeling.makeGraph(selected_options)
    graphjson = fig.to_json()

    return render_template('index.html', graphJSON = graphjson)

app.run(host = "0.0.0.0", port = 80)