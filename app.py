from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import numpy as np

app = Flask(__name__)
battingAll = pd.read_csv("./Python/Fangraphs/battingAllUvc.csv")

goodBatters = ["Bryce Harper", "Manny Machado", "Mike Trout", "Mookie Betts", "Jose Altuve"]
goodBattersValues = [16.297, 15.126, 40.540, 18.713, 18.373]

#==========================
# ROUTES
#==========================

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
    if checkValid(yearlyStats):
        totalPlayers = battingAll.drop_duplicates(subset=['Name'], keep="first")
        ops = [stat[34] for stat in yearlyStats]
        current_wrc = yearlyStats[-1][44]
        wrc = [stat[44] for stat in yearlyStats]
        years = [stat[6] for stat in yearlyStats]
        team = yearlyStats[-1][7]
        all_wrc = [stat[44] for stat in battingAll.values]
        current_ops = yearlyStats[-1][34]
        all_ops = [stat[34] for stat in battingAll.values]
        spd = [stat[36] for stat in yearlyStats]
        current_spd = yearlyStats[-1][36]
        all_spd = [stat[36] for stat in battingAll.values]
        uvc = yearlyStats[-1][47]
        uvcBar = generateUVCBarStatistics(request.form["playerName"], uvc)

        return render_template('player.html', 
            valid=checkValid(yearlyStats),
            uvc_rounded="{0:.2f}".format(uvc),
            uvc_players=uvcBar[0],
            uvc_values=uvcBar[1],
            uvc_percentile=generatePercentile(uvc, totalPlayers['UvC']),
            playerName=request.form["playerName"], 
            ops=ops, 
            spd=spd,
            years=years, 
            team=team, 
            wrc=wrc, 
            wrcRank=generateWRCRank(current_wrc), 
            wrcPercentile=generatePercentile(current_wrc, all_wrc),
            opsRank=generateOPSRank(current_ops),
            opsPercentile=generatePercentile(current_ops, all_ops),
            spdRank=generateSPDRank(current_spd),
            spdPercentile=generatePercentile(current_spd, all_spd))

    else:
        return render_template('player.html', 
            valid=checkValid(yearlyStats))


#==========================
# HELPER METHODS
#==========================

def generateWRCRank(value):
    if value >= 135:
        return "great"
    elif value >= 110 and value < 135:
        return "good"
    elif value >= 90 and value < 110:
        return "average"
    elif value >= 65 and value < 90:
        return "below average"
    else:
        return "awful"

def generateOPSRank(value):
    if value >= .85:
        return "great"
    elif value >= .766 and value < .85:
        return "good"
    elif value >= .7 and value < .766:
        return "average"
    elif value >= .6 and value < .7:
        return "below average"
    else:
        return "awful"

def generateSPDRank(value):
    if value >= 6.5:
        return "great"
    elif value >= 5.5 and value < 6.5:
        return "good"
    elif value >= 4.5 and value < 5.5:
        return "average"
    elif value >= 3.5 and value < 4.5:
        return "below average"
    else:
        return "awful"

def generatePercentile(value, series):
    percent = float(len([score for score in series if score < value])) / len(series) * 100
    return "{0:.2f}%".format(percent) 

def checkValid(df):
    if len(df) == 0:
        return False
    else:
        return True

def generateUVCBarStatistics(playerName, uvc):
    if playerName in goodBatters:
        return goodBatters, goodBattersValues
    else:
        return [str(playerName)] + goodBatters, [uvc] + goodBattersValues