import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'TSS_gaming_rocks'


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/teams', methods=['GET', 'POST'])
def teamsView():
    if request.method == 'POST' and 'file' in request.files:
        data_file = request.files['file']
        # original_data = pd.read_csv("file_test.csv")
        # 'TEAM NAME', 'Player 1 Name(CAPTAIN)', 'Player 1 in-game name with tag',	'Player 1 Discord id with tag'
        original_data = pd.read_csv(data_file)
        teams_data = original_data.to_dict()
        session['data'] = teams_data
        print(teams_data)
        num_teams = len(teams_data['TEAM NAME'])
    return render_template('teams.html', teams=teams_data, num_teams=num_teams, file=data_file)


@app.route('/pairing', methods=['GET', 'POST'])
def pairing():
    # if request.method == 'POST' and 'file' in request.files:
    #data_file = request.files['file']
    teams_data = session['data']
    original_data = pd.DataFrame.from_dict(teams_data)
    # original_data = pd.read_csv("file_test.csv")

    altered_data = process(original_data)

    altered_data.to_csv("altered_data.csv")

    # print(altered_data.head())
    # test = pd.read_csv('alt_data.csv')
    # alt_data = test.sort_values(by = ['Platinum', 'Gold', 'Silver', 'Bronze', 'Iron'], ascending = False)
    # test_pairing_list = alt_data['Team Name'].tolist()
    pairing_list = altered_data['Team Name'].tolist()
    # print(pairing_list)
    # print(pairing_list[0])
    # return render_template('pairing.html')
    # return render_template('test_bracket.html')
    return render_template('test_brackets2.html', pairing=pairing_list)


def process(data):

    alt_data = pd.DataFrame(
        columns=['Team Name', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron'])

    for i in data.index:
        Platinum = 0
        Gold = 0
        Silver = 0
        Bronze = 0
        Iron = 0
        for j in range(1, 6):
            if "PLATINUM" in data['Player {} Rank'.format(j)][i]:
                Platinum = Platinum + 1
            if "GOLD" in data['Player {} Rank'.format(j)][i]:
                Gold = Gold + 1
            if "SILVER" in data['Player {} Rank'.format(j)][i]:
                Silver = Silver + 1
            if "BRONZE" in data['Player {} Rank'.format(j)][i]:
                Bronze = Bronze + 1
            if "IRON" in data['Player {} Rank'.format(j)][i]:
                Iron = Iron + 1
        alt_data.loc[i] = [data['TEAM NAME'][i],
                           Platinum, Gold, Silver, Bronze, Iron]
    alt_data = alt_data.sort_values(
        by=['Platinum', 'Gold', 'Silver', 'Bronze', 'Iron'], ascending=False)
    return (alt_data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
