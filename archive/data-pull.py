import requests

# Gets the Active Tournament
url = "https://24live.com/api/tournament/22357"

querystring = {"lang":"en","section":"all","seasonId":"70665","short":"0","limit":"10","sid":"70523","id":"1011803"}

payload = ""
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.8",
    "cookie": "XSRF-TOKEN=voSSbVIw5DNa3JSWXp0WVEo9RAzjeAptwjM9rqWk; laravelsession=LdRfSKOoOF4OaHZ2nnpcnUGN5FiYQZYWM6KGoHOH",
    "priority": "u=1, i",
    "referer": "https://24live.com/page/sport/event/table-tennis-22/22357?lang=en",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

json_resp = response.json()

# json["data"]["not_started"] --> This get all the upcoming matches for the current time

print(len(json_resp["data"]["not_started"]))
