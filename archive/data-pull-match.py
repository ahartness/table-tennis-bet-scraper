import requests

url = "https://24live.com/api/match/"

querystring = {"lang":"en","short":"0","h2hlimit":"50"}
match_id = "4909569"

payload = ""
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

response = requests.request("GET", url + match_id, data=payload, headers=headers, params=querystring)

json_resp = response.json()

# json_resp["h2h"]["total"]["h2h"] --> this is all the Head 2 Head stats between the match players
#
# Using the Above Array And Looping through each element:
# Total score of a match: elem['score']['home_team_normal_time'] + elem['score']['away_team_normal_time']
# Total Number of Rounds:  elem['score']['home_team'] + elem['score']['away_team']
# Date of Match:  elem["date"]
#
# time.strptime(elem['date'][0:10], '%Y-%m-%d')
# time.strptime("2024-09-01", '%Y-%m-%d')


print(json_resp["h2h"]["total"]["h2h"])
