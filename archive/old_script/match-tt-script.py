import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Enter Variables HERE
# ------------------------
over_target = 69
match_id = '4940697'
match_amount = 20
date_from = '2024-07-01'
# ------------------------

format = '%Y-%m-%dT%H:%M'
score_array = []
total_counter = 0
over_counter = 0
over_percent = 0
four_round_counter = 0
five_round_counter = 0
four_plus_percent = 0
five_round_percent = 0
four_round_percent = 0

data_array = []
schedule_url = "https://24live.com/api/tournament/22357"

match_url = "https://24live.com/api/match/"

querystring = {"lang":"en","section":"all","seasonId":"70665","short":"0","limit":match_amount,"sid":"70523","id":"1011803"}
match_querystring = {"lang":"en","short":"0","h2hlimit":match_amount}

schedule_payload = ""
match_payload = ""

compare_date = time.strptime(date_from, '%Y-%m-%d')

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

match_req_url = match_url + match_id

match_resp = requests.request("GET", match_req_url, data=match_payload, headers=headers, params=match_querystring)

match_json_resp = match_resp.json()

if len(match_json_resp["h2h"]["total"]["h2h"]) > 0:
    for elem in match_json_resp["h2h"]["total"]["h2h"]:
        newdate1 = time.strptime(elem['date'][0:10], '%Y-%m-%d')
        if elem['score']['home_team_normal_time'] != None:
            if newdate1 > compare_date:
                total_counter += 1
                temp_score = elem['score']['home_team_normal_time'] + elem['score']['away_team_normal_time']
                temp_round = elem['score']['home_team'] + elem['score']['away_team']

                if temp_score > over_target:
                    over_counter += 1

                if temp_round == 4:
                    four_round_counter += 1

                if temp_round == 5:
                    five_round_counter += 1

if  total_counter > 0:
    over_percent = (over_counter / total_counter) * 100
    four_round_percent = (four_round_counter / total_counter) * 100
    five_round_percent = (five_round_counter / total_counter) * 100
    four_plus_percent = ((four_round_counter + five_round_counter) / total_counter) * 100

# print(match_json_resp)
# print(four_round_counter)

score_array.append({
    "id": match_json_resp["id"],
    "date": (datetime.strptime(match_json_resp["start_date"][0:16], format) - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
    "home_team": match_json_resp['participants'][0]['name_short'],
    "away_team": match_json_resp['participants'][1]['name_short'],
    "total_h2h": total_counter,
    "four_plus": f"{(four_round_counter + five_round_counter)} / {total_counter}",
    "four_plus_percent": f"{four_plus_percent:.2f}%",
    "over_num": f"{over_counter} / {total_counter}",
    "over_pecent": f"{over_percent:.2f}%",
    "over_amount": over_target
})

df = pd.json_normalize(score_array);

df.to_csv('tt-individual-match-data-output.csv', index=False)

# print("Over 74.5 Percentage: ")
# print(f"{over_percent:.2f}%")
# print(f"{over_counter} / {total_counter}")
# print("4 plus Percentage: ")
# print(f"{four_plus_percent:.2f}%")
# print(f"{four_round_counter + five_round_counter} / {total_counter}")
# print("4 Rounds Percentage: ")
# print(f"{four_round_percent:.2f}%")
# print(f"{four_round_counter} / {total_counter}")
# print("5 Rounds Percentage: ")
# print(f"{five_round_percent:.2f}%")
# print(f"{five_round_counter} / {total_counter}")
# print(score_array)
