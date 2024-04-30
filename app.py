from flask import Flask, render_template, request
from services import topic_modeling

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    philosophers = ['confucius', 'nietzsche', 'kant', 'laozi', 'sunzi', 'plato']
    settings = ['wordcount', 'chunkcount', 'evenchunking']

    selected_philosophers = [request.form[philosopher] for philosopher in philosophers if request.form.get(philosopher)]
    selected_settings = [request.form[setting] for setting in settings if request.form.get(setting)]

    print(selected_philosophers)
    print(selected_settings)

    valid_input = True

    if not selected_philosophers:
        valid_input = False
    if 'evenchunking' in selected_settings:
        if len(selected_settings) < 3:
           valid_input = False
    elif len(selected_settings) < 2:
        valid_input = False

    if not valid_input:
        return render_template('index.html')
        
    fig, vocab = topic_modeling.makeGraph(selected_philosophers, selected_settings)
    graphjson = fig.to_json()

    return render_template('index.html', graphJSON = graphjson, vocabulary = f"Vocabulary: [{vocab}]")

# app.run(host = "0.0.0.0", port = 80)