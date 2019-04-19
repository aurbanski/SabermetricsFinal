from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import numpy as np

app = Flask(__name__)
battingAll = pd.read_csv("./Python/Fangraphs/battingAll.csv")

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
    yearlyStats = list(battingAll.loc[battingAll["Name"] == request.form["playerName"]].values)
    battingAverage = [stat[27] for stat in yearlyStats]
    years = [stat[6] for stat in yearlyStats]
    team = yearlyStats[-1][7]
    return render_template('player.html', playerName=request.form["playerName"], yearlyStats=yearlyStats, battingAverage=battingAverage, years=years, team=team) 