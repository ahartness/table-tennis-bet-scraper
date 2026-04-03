import schedule
from chump import Application
import csv
import json
from datetime import datetime, timedelta
import time
from fullttscript import run_data_script

def first_set_job():
    print("----Starting First Set Job----")
    app = Application("hidden")
    private = app.get_user("hidden")

    message = ''

    with open('data/tt-first-set-plays.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    time_now = datetime.strptime(str(datetime.now())[0:16], '%Y-%m-%d %H:%M')

    for match in data:
        time_compare = datetime.strptime(match["date"], '%Y-%m-%d %I:%M%p')
        bet_amt = '.5u'

        if((time_now < (time_compare + timedelta(minutes=1)) and time_now > (time_compare - timedelta(minutes=1))) and float(match['four_round']) >= .85):
            print(f"Match Starting! Sending notification for - {match['slug']}")
            message = private.send_message(
                title= f"Match Starting Now - 4+ Games",
                message=f"{match['home_player']} vs. {match['away_player']}\n4+ Games -- Bet Amount: {bet_amt}\nFour or More: {match['over_four']} -- {match['four_rate']}",
            )


def four_more_job():
    print("----Starting Four or More Job-----")
    app = Application("ahey4sok8gixmc2e5xqfynky4ah1x4")
    private = app.get_user("u6ypbjv8t8jqzoodhktnkriw5bjz12")

    with open('data/tt-four-or-more-plays-updated.csv', 'r') as csvfile:
           reader = csv.DictReader(csvfile)
           data = [row for row in reader]

    time_now = datetime.strptime(str(datetime.now())[0:16], '%Y-%m-%d %H:%M')

    for match in data:
        time_compare = datetime.strptime(match["date"], '%Y-%m-%d %I:%M%p')
        bet_amt = ".75u/1.25u"
        # print(f"Checking match: {match['date']} - {match['slug']}")
        # print(time_now.strftime('%Y-%m-%d %I:%M%p'))
        # print(match["date"])
        if(float(match['four_round']) >= .95):
            bet_amt = ".8u/1.7u"

        if((time_now < (time_compare + timedelta(minutes=1)) and time_now > (time_compare - timedelta(minutes=1))) and float(match['four_round']) >= .85):
            print(f"Match Starting! Sending notification for - {match['slug']}")
            message = private.send_message(
                title= f"Match Starting Now - 4+ Games",
                message=f"{match['home_player']} vs. {match['away_player']}\n4+ Games -- Bet Amount: {bet_amt}\nFour or More: {match['over_four']} -- {match['four_rate']}",
            )
        elif((time_now < (time_compare - timedelta(minutes=4)) and time_now > (time_compare - timedelta(minutes=6))) and float(match['four_round']) >= .85):
            print(f"Match Starting! Sending notification for - {match['slug']}")
            #message = private.send_message(
            #    title= f"Match Starting In 5 Minutes - 4+ Games",
            #    message=f"{match['home_player']} vs. {match['away_player']}\n4+ Games -- Bet Amount: {bet_amt}\nFour or More: {match['over_four']} -- {match['four_rate']}",
            #)

def job():
    # def send_notification():
    # Pull out these values if private repo is removed
    print("------Checking for Over/Under Notifications------")
    print(datetime.now())
    try:
        app = Application("ahey4sok8gixmc2e5xqfynky4ah1x4")
        # print(app.is_authenticated)

        user = app.get_user("gzwxnns1a979f3nu4dwjbp87dxf1fm")
        # print(user.is_authenticated, user.devices)

        # Open the CSV file
        with open('data/tt-best-plays-updated.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]

        time_now = datetime.strptime(str(datetime.now())[0:16], '%Y-%m-%d %H:%M')

        for match in data:
            time_compare = datetime.strptime(match["date"], '%Y-%m-%d %I:%M%p')
            # print(f"Checking match: {match['date']} - {match['slug']}")
            # print(time_now.strftime('%Y-%m-%d %I:%M%p'))
            # print(match["date"])
            if(time_now < (time_compare) and time_now > (time_compare - timedelta(minutes=2))):
                print(f"Match Starting! Sending notification for - {match['slug']}")
                user.send_message(
                    title= f"Match Starting Now",
                    message=f"{match['home_player']} vs. {match['away_player']}\nBet Amount: {match['bet_amt']} @ {match['target']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_5']} -- {match['last_10']} -- {match['last_15']} -- {match['last_20']} -- {match['total_over']}",
                )
            # elif(time_now < (time_compare - timedelta(minutes=34)) and time_now > (time_compare - timedelta(minutes=36)) and match['target'] == '74.5'):
            #     print(f"Betting Opening Soon! Sending notification for - {match['slug']}")
            #     user.send_message(
            #         title= f"Total Bet Opens in 5 minutes on FanDuel",
            #         message=f"{match['home_player']} vs. {match['away_player']}\nBet Amount: {match['bet_amt']} @ {match['target']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_5']} -- {match['last_10']} -- {match['last_15']} -- {match['last_20']} -- {match['total_over']}",
            #     )
            elif(time_now < (time_compare - timedelta(minutes=29)) and time_now > (time_compare - timedelta(minutes=31)) and match['target'] == '74.5'):
                print(f"Betting Has Opened! Sending notification for - {match['slug']}")
                user.send_message(
                    title= f"Total Bet Open NOW on FanDuel",
                    message=f"{match['home_player']} vs. {match['away_player']}\nBet Amount: {match['bet_amt']} @ {match['target']}\nConfidence: {match['confidence']} -> {match['ci_interval']}\nHead 2 Head: {match['last_5']} -- {match['last_10']} -- {match['last_15']} -- {match['last_20']} -- {match['total_over']}",
                )
            # else:
            #     print("Match is not starting yet")
    except NameError:
        print("Notification Check Failed")
        print(NameError)
    print("-----Notification Check Complete-----")


# Schedule the job
schedule.every().minute.at(":35").do(job)
# schedule.every().minute.at(":35").do(four_more_job)
# schedule.every().minute.at(":55").do(first_set_job)
# schedule.every(8).hours.at("10:00").do(run_data_script)
schedule.every().day.at("06:02", "US/Eastern").do(run_data_script)
# schedule.every().day.at("11:02", "US/Eastern").do(run_data_script)
# schedule.every().day.at("16:32", "US/Eastern").do(run_data_script)
# schedule.every().day.at("21:32", "US/Eastern").do(run_data_script)

while True:
    schedule.run_pending()
    time.sleep(1)
