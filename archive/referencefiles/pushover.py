from chump import Application
import csv
import json
from datetime import datetime, timedelta
import time

# def send_notification():
# Pull out these values if private repo is removed
app = Application("ahey4sok8gixmc2e5xqfynky4ah1x4")
print(app.is_authenticated)

user = app.get_user("u6ypbjv8t8jqzoodhktnkriw5bjz12")
print(user.is_authenticated, user.devices)

# Open the CSV file
with open('tt-best-plays-updated.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

print(data[0])

time_now = datetime.strptime(str(datetime.now())[0:16], '%Y-%m-%d %H:%M')

for match in data:
    time_compare = datetime.strptime(match["date"], '%Y-%m-%d %I:%M%p')
    print(f"Checking match: {match['date']} - {match['slug']}")
    print(match["date"])
    if(time_now < (time_compare + timedelta(minutes=1)) and time_now > (time_compare - timedelta(minutes=1))):
        message = user.send_message(
            title= f"Match Starting Now",
            message=f"{match['home_player']} vs. {match['away_player']}\nOVER 74.5 -- Bet Amount: {match['bet_amt']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_10']} -- {match['last_20']} -- {match['total_over']}",
        )
    elif(time_now < (time_compare - timedelta(minutes=34)) and time_now > (time_compare - timedelta(minutes=36))):
        message = user.send_message(
            title= f"Total Bet Opens in 5 minutes on FanDuel",
            message=f"{match['home_player']} vs. {match['away_player']}\nOVER 74.5 -- Bet Amount: {match['bet_amt']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_10']} -- {match['last_20']} -- {match['total_over']}",
        )
    elif(time_now < (time_compare - timedelta(minutes=29)) and time_now > (time_compare + timedelta(minutes=31))):
        message = user.send_message(
            title= f"Total Bet Open NOW on FanDuel",
            message=f"{match['home_player']} vs. {match['away_player']}\nOVER 74.5 -- Bet Amount: {match['bet_amt']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_10']} -- {match['last_20']} -- {match['total_over']}",
        )

# return f"{message.is_sent} - {message.id}"
