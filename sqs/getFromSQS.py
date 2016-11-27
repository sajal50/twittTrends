from multiprocessing import Pool, TimeoutError
import time
import os
import multiprocessing
import boto3
import config as Config
import json
from watson_developer_cloud import AlchemyLanguageV1


sqs = boto3.resource('sqs')
SQS_QUEUE_NAME=Config.SQS_QUEUE
alchemy_language = AlchemyLanguageV1(api_key=Config.ALCHEMY_API_KEY)


def getFromSQS():
	queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
	for message in queue.receive_messages():
		tweet = json.loads(message.body)
        if tweet is not None :
            #getting sentiment

            result = json.loads(json.dumps( alchemy_language.sentiment( text = tweet['text']), indent = 2))
            docSentiment =  result['docSentiment']
            sentiment = docSentiment['type']
            tweet['sentiment'] = sentiment
            tweet = json.dumps(tweet)
            print tweet

            #pushing to sns

            client = boto3.client('sns')
            response = client.publish(
                TargetArn= Config.SNS_ARN,
                Message=json.dumps({'default': tweet}),
                MessageStructure='json'
            )

            message.delete()

if __name__ == '__main__':
    pool = Pool(processes=4)
    while 1:

    	multiple_results = [pool.apply_async(getFromSQS, ()) for i in range(4)]
    	#print [res.get(timeout=1) for res in multiple_results]
    	time.sleep(2)



