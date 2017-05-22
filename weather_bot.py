# Simple weather bot for Reddit
# Responds to !Weather XXXXX, where XXXXX is a 5 tuple of integers for ZIP

import praw
import time
import config
import requests
import re
import database_connector

SUBREDDIT_USED = "test"
COUNTRY = "us"


# Authenticate to Reddit using praw
def authenticate():
    print("Script is now authenticating...")
    reddit = praw.Reddit('weatherBot', user_agent='Mikes Weather Bot')
    print("Autneticated as {}".format(reddit.user.me()))
    return reddit

def check_comment(comment):
    zipCode = -1
    commandComment = re.search('!weather [0-9]{5}', comment)
    if(commandComment):
        zipCode = re.search('\d+', comment)
    return zipCode

def get_weather(zipCode):
    URL = "http://api.openweathermap.org/data/2.5/weather?zip={},{}&units=imperial&APPID={}".format(zipCode,COUNTRY,config.OpenWeatherKey)
    # print(URL)
    weatherStatus = requests.get(URL).json()['weather'][0]['main']
    weatherTemp = requests.get(URL).json()['main']['temp']
    weatherString = "Currently in {} weather is: {}, with a tempature of {} degrees F.".format(zipCode,weatherStatus,weatherTemp)
    return weatherString

def run_bot(reddit):
    print("Now checking the newest 50 comments in {}".format(SUBREDDIT_USED))
    for comment in reddit.subreddit(SUBREDDIT_USED).comments(limit=50):
            zipCode = check_comment(comment.body)
            if(zipCode != -1):
                comment.reply(get_weather(zipCode[0]))
                print("Script has replied to a comment.")
                database_connector.insert(comment.id)
    print("Sleeping for 1 minute.")
    time.sleep(60)


def main():
    reddit = authenticate()
    #database_connector.displayAll()
    while True:
        run_bot(reddit)

if __name__ == '__main__':
    main()
