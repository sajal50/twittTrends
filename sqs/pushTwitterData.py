#! /usr/bin/python
''' The script is used to pull data from twitter using twython and dumping the data into elasticsearch'''
import boto3
import config as Config #Using config file to read the config settings from a separate config file.
from twython import Twython
from datetime import datetime
import json

TWITTER_APP_KEY = Config.TWITTER_APP_KEY
TWITTER_APP_KEY_SECRET = Config.TWITTER_APP_KEY_SECRET
TWITTER_ACCESS_TOKEN = Config.TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET = Config.TWITTER_ACCESS_TOKEN_SECRET

SQS_QUEUE_NAME=Config.SQS_QUEUE

twitterauth = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
print (queue.url)


def pull_tweets(keyword):
    print "D"
    search = twitterauth.search(q=keyword,count=100)
    tweets = []
    tweets = search['statuses']
    for tweet in tweets:

        if tweet['geo'] != None:
            # language=guess_language(tweet['text'])
            # print language
            print tweet['user']['lang']
            if tweet['user']['lang']=='en':

                print "YES"
                text = tweet['text'].lower().encode('ascii','ignore').decode('ascii')
                print text
                index = tweet['id']
                print index
                coordinates = tweet['geo']['coordinates']
                print coordinates
                message={
                'id':index,
                'text':text,
                'coordinates':coordinates,
                'sentiment':''
                }
                temp=json.dumps(message)
                print temp
                response = queue.send_message(MessageBody=temp)




def twittmap():
    try:
        for i in range(1,50):
            pull_tweets('java')
            pull_tweets('love')
            pull_tweets('trump')
            pull_tweets('clinton')
            pull_tweets('india')
            pull_tweets('diwali')
            pull_tweets('movie')
            pull_tweets('music')
    except:
	#pass
	return

twittmap()
pull_tweets
