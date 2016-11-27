from multiprocessing import Pool, TimeoutError, Lock
import threading
import time
import os
import multiprocessing
from watson_developer_cloud import AlchemyLanguageV1
import boto3
import config as Config #Using config file to read the config settings from a separate config file.
from kafka import KafkaConsumer
import json

KAFKA_HOST = 'localhost:9092'
TOPIC = 'test'
lock = Lock() 
alchemy_language = AlchemyLanguageV1(api_key=Config.ALCHEMY_API_KEY)


def getFromKafka():
    lock.acquire()

    consumer = KafkaConsumer(TOPIC, bootstrap_servers=[KAFKA_HOST],consumer_timeout_ms=10000)
    for message in consumer:

        tweet = json.loads(message.value)
        if tweet is not None :
            #getting sentiment

            result = json.loads(json.dumps( alchemy_language.sentiment( text = tweet['text']), indent = 2))
            docSentiment =  result['docSentiment']
            sentiment = docSentiment['type']
            tweet['sentiment'] = sentiment
            tweet = json.dumps(tweet)
            print tweet
    
            client = boto3.client('sns')
            response = client.publish(
                TargetArn=Config.SNS_ARN,
                Message=json.dumps({'default': tweet}),
                MessageStructure='json'
            )

    lock.release()
	    
if __name__ == '__main__':
    #getFromKafka()

    pool = Pool(processes=4)              # start 4 worker processes
    

    while 1:
    	multiple_results = [pool.apply_async(getFromKafka, ()) for i in range(4)]
    	print [res.get(timeout=100) for res in multiple_results]
    	time.sleep(2)
    
