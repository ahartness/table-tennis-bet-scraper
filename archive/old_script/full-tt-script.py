import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Input Variables
# -----------------------
match_amount = 100
h2h_limit = 20
over_target = 74
date_from = "2024-08-01"
over_limit = 69
under_limit = 25
# -----------------------

format = '%Y-%m-%dT%H:%M'
compare_date = time.strptime(date_from, '%Y-%m-%d')

data_array = []
best_plays_array = []
four_more_array = []
schedule_url = "https://24live.com/api/tournament/22357"
match_url = "https://24live.com/api/match/"

querystring = {"lang":"en","section":"all","seasonId":"70665","short":"0","limit":match_amount,"sid":"70523","id":"1011803"}
match_querystring = {"lang":"en","short":"0","h2hlimit":h2h_limit}

schedule_payload = ""
match_payload = ""

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.8",
    "cookie": "XSRF-TOKEN=ivznu5xPC6ZyfM4LnOpoFK1yGHgkuVWzcdUOocXD; laravelsession=vYfBdrd9ybGDVg9rc2a8tgxMpRIqp7RVRNo2gg9U",
    "priority": "u=1, i",
    "referer": "https://24live.com/page/sport/event/table-tennis-22/22357",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

schedule_resp = requests.request("GET", schedule_url, data=schedule_payload, headers=headers, params=querystring)

schedule_json = schedule_resp.json()

for match in schedule_json["data"]["not_started"]:
    match_req_url = match_url + str(match["id"])
    total_counter = 0
    over_counter = 0
    four_round_counter = 0
    five_round_counter = 0
    home_team_wins = 0
    away_team_wins = 0
    out_of_5 = 0
    out_of_10 = 0
    out_of_15 = 0
    out_of_20 = 0
    out_of_25 = 0
    out_of_30 = 0

    match_resp = requests.request("GET", match_req_url, data=match_payload, headers=headers, params=match_querystring)

    match_json_resp = match_resp.json()

    if len(match_json_resp["h2h"]["total"]["h2h"]) > 0:
        for index, elem in enumerate(match_json_resp["h2h"]["total"]["h2h"]):
            newdate1 = time.strptime(elem['date'][0:10], '%Y-%m-%d')
            if elem['score']['home_team_normal_time'] != None:
                if newdate1 > compare_date:
                    total_counter += 1
                    if elem['score']['home_team'] > elem['score']['away_team']:
                        home_team_wins += 1
                    else:
                        away_team_wins += 1

                    temp_score = elem['score']['home_team_normal_time'] + elem['score']['away_team_normal_time']
                    temp_round = elem['score']['home_team'] + elem['score']['away_team']

                    if temp_score > over_target:
                        over_counter += 1
                        if(index < 5):
                            out_of_5 += 1
                        elif(index >= 5 and index < 10):
                            out_of_10 += 1
                        elif(index >= 10 and index < 15):
                            out_of_15 += 1
                        elif(index >= 15 and index < 20):
                            out_of_20 += 1
                        elif(index >= 20 and index < 25):
                            out_of_25 += 1
                        else:
                            out_of_30 += 1

                    if temp_round == 4:
                        four_round_counter += 1

                    if temp_round == 5:
                        five_round_counter += 1

    if (total_counter > 0):
        percent_for_four = ((five_round_counter + four_round_counter) / total_counter) * 100
        if(percent_for_four >= 70) and total_counter >= 10:
            four_bet_amount_game_2 = .25
            four_bet_amount_game_3 = .5

            four_hit_rate = ((four_round_counter + five_round_counter) / total_counter) * 100

            if (four_hit_rate >= 70 and four_hit_rate < 75):
                four_bet_amount_game_2 = .25
                four_bet_amount_game_3 = .5
            elif (four_hit_rate >= 75 and four_hit_rate < 80):
                four_bet_amount_game_2 = .3
                four_bet_amount_game_3 = .7
            elif (four_hit_rate >= 80 and four_hit_rate < 85):
                four_bet_amount_game_2 = .4
                four_bet_amount_game_3 = .85
            elif (four_hit_rate >= 85 and four_hit_rate < 90):
                four_bet_amount_game_2 = .5
                four_bet_amount_game_3 = 1
            elif (four_hit_rate >= 90):
                four_bet_amount_game_2 = .5
                four_bet_amount_game_3 = 1.25
            else:
                four_bet_amount_game_2 = .25
                four_bet_amount_game_3 = .5

            four_more_array.append({
                            "id": match["id"],
                            "date": (datetime.strptime(match["start_date"][0:16], format) - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                            "home_team": match["participants"][0]["name_short"],
                            "away_team": match["participants"][1]["name_short"],
                            "total_h2h": total_counter,
                            "four_more": f"{(four_round_counter + five_round_counter)} / {total_counter}",
                            "four_more_%": f"{(((four_round_counter + five_round_counter) / total_counter) * 100):.2f}%",
                            "game_2_bet": f"{four_bet_amount_game_2}u",
                            "game_3_bet": f"{four_bet_amount_game_3}u",
                            "divider": "#######",
                            "home_wins": home_team_wins,
                            "away_wins": away_team_wins,
                        })

    if (total_counter > 0):
        percent_for_over = (over_counter / total_counter) * 100
        percent_for_four = ((five_round_counter + four_round_counter) / total_counter) * 100

        five_index = (out_of_5 / 5) * .10
        ten_index = ((out_of_5 + out_of_10) / 10) * .15
        fifteen_index = ((out_of_5 + out_of_10 + out_of_15) / 15) * .30
        twenty_index = ((out_of_5 + out_of_10 + out_of_15 + out_of_20) / 20) * .45

        # if (percent_for_over > over_limit or percent_for_over < under_limit or percent_for_four > 79) and total_counter >= 10:
        if ((((out_of_5 + out_of_10) / 10) * 100) >= 70 or (((out_of_5 + out_of_10) / 10) * 100) <= 10) and total_counter >= 10:
            hit_rate = (over_counter / total_counter) * 100
            bet_amount = .5

            if (hit_rate >= 65 and hit_rate < 70):
                bet_amount = .75
            elif (hit_rate >= 70 and hit_rate < 79):
                bet_amount = 1
            elif (hit_rate >= 80 and hit_rate < 85):
                bet_amount = 1.25
            elif (hit_rate >= 85 and hit_rate < 90):
                bet_amount = 1.5
            elif (hit_rate >= 90 and hit_rate < 95):
                bet_amount = 1.75
            elif (hit_rate >= 95):
                bet_amount = 2
            else:
                bet_amount = .75

            best_plays_array.append({
                "id": match["id"],
                "date": (datetime.strptime(match["start_date"][0:16], format) - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                "home_team": match["participants"][0]["name_short"],
                "away_team": match["participants"][1]["name_short"],
                "total_h2h": total_counter,
                "matches_over": f"{over_counter} / {total_counter}",
                "hit_rate": f"{((over_counter / total_counter) * 100):.2f}%",
                "target": str(over_target) + ".5",
                "play": "OVER" if percent_for_over > over_limit else "UNDER",
                "bet_amount": f"{bet_amount}u",
                "divider": "#######",
                "Last 5": f"{out_of_5} / 5",
                "Last 10": f"{out_of_5 + out_of_10} / 10",
                "Last 15": f"{out_of_10 + out_of_5 + out_of_15} / 15",
                "Last 20": f"{out_of_15 + out_of_5 + out_of_10 + out_of_20} / 20",
                "Index": f"{(five_index + ten_index + fifteen_index + twenty_index) * 100:.2f}%",
                "home_wins": home_team_wins,
                "away_wins": away_team_wins,
                "four_more": f"{(four_round_counter + five_round_counter)} / {total_counter}",
                "four_more_%": f"{(((four_round_counter + five_round_counter) / total_counter) * 100):.2f}%",
            })

    if total_counter > 0:
        data_array.append({
            "id": match["id"],
            "date": (datetime.strptime(match["start_date"][0:16], format) - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
            "home_team": match["participants"][0]["name_short"],
            "away_team": match["participants"][1]["name_short"],
            "total_h2h": total_counter,
            "home_wins": home_team_wins,
            "away_wins": away_team_wins,
            "four_more": f"{(four_round_counter + five_round_counter)} / {total_counter}",
            "four_more_%": f"{(((four_round_counter + five_round_counter) / total_counter) * 100):.2f}%",
            "matches_over": f"{over_counter} / {total_counter}",
            "percent_over": f"{((over_counter / total_counter) * 100):.2f}%",
            "over_target": over_target,
            "home_win_%": f"{((home_team_wins / (away_team_wins + home_team_wins))*100):.2f}%"
            # "four_round": four_round_counter,
            # "four_%": f"{((four_round_counter / total_counter) * 100):.2f}%",
            # "five_round": five_round_counter,
            # "five_%": f"{((five_round_counter / total_counter) * 100):.2f}%",
        })

df = pd.json_normalize(data_array)

df.to_csv('tt-match-data-output.csv', index=False)

df = pd.json_normalize(best_plays_array)

df.to_csv('tt-best-plays-output.csv', index=False)

df = pd.json_normalize(four_more_array)

df.to_csv('tt-over-four-output.csv', index=False)
