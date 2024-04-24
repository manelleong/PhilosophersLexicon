from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    philosophers = ['confucius', 'nietzsche', 'kant']

    selected_options = [request.form[philosopher] for philosopher in philosophers if request.form.get(philosopher)]

    print(selected_options)

    return render_template('index.html')

app.run(host = "0.0.0.0", port = 80)