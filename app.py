from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home_screen():
    return render_template("home.html")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/test')
def test():
    return "test"

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/player', methods=['POST'])
def player():
    return render_template('player.html', playerName=request.form["playerName"]) 