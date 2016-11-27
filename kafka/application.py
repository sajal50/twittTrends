import certifi
import sys
import os
import json
import time
import config as Config
from flask import Flask
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, g, redirect, Response, make_response, jsonify
from elasticsearch import *
es = Elasticsearch([Config.ES])

application = Flask(__name__)  
app = application

es.indices.create(index='twitter', ignore=400)


@app.route ('/sns', methods=['POST'])
def sns() :

    data = request.data
    dataDict = json.loads(data)


    if dataDict['Type'] == "SubscriptionConfirmation" :
        print dataDict['SubscribeURL']  
    else :

        tweet = dataDict['Message']
        #print tweet
        res = es.index(index="twitter",doc_type='twitter', body= tweet)
        #print(res['created'])


    return Response(json.dumps({"message" : "sajal"}), content_type='application/json')

@app.route('/search/<keyword>', methods=['GET'])
def search(keyword):

    try:

        res = es.search(index="twitter",scroll='1s',search_type='scan',size=10000, body={"query": {"match": { "text": { "query": keyword, "operator": "or" } } } })
        output=[]
        tweets=[]
        scroll_size=res["hits"]["total"]
        #output.append(scroll_size)
        while scroll_size>0:
            scroll_id=res['_scroll_id']
            rs=es.scroll(scroll_id=scroll_id,scroll='100s')
            tweets+=rs['hits']['hits']
            scroll_size=len(res['hits']['hits'])
        for doc in tweets:
                message={"coordinates":doc['_source']['coordinates'],"sentiment":doc['_source']['sentiment']}
                output.append(message)
        return Response(json.dumps(output), content_type='application/json')
        
    except Exception as e:
        pass


@app.route('/user', methods=['GET'])
def user():
    return render_template('index.html')

if __name__ == "__main__":         
        app.run(host='0.0.0.0',threaded=True, debug =True)