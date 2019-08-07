import base64
import requests
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from datetime import datetime
from src import config as config


engine = psycopg2.connect(
    database="postgres",
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port
)

cursor = engine.cursor()


def pull(engine, conn):
    panel = conn
    cursor = engine

    analyser = SentimentIntensityAnalyzer()
    # Twitter auth credentials
    client_id = config.client_id
    client_secret = config.client_secret

    ############ AUTH #############

    # Reformat the keys and encode them
    key_secret = '{}:{}'.format(config.client_id, config.client_secret).encode('ascii')

    # Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)

    # Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']
    ############ /AUTH #############

    print(auth_resp.status_code)

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    search_params = {
        'q': 'Bitcoin',
        'result_type': 'recent',
        'count': '100',

    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    json = search_resp.json()
    msg = json['statuses'][0]['text']

    pos, neg, neut = 0

    for i in json['statuses']:
        tweet = i['text']
        vs = analyser.polarity_scores(tweet)
        date = datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        compound = vs['compound']
        pol="n/a"
        if compound >=0.05:
            pos +=1
            pol = "pos"
        elif compound > -0.05 and compound < 0.05:
            neut +=1
            pol = "neu"
        elif compound <=0.05:
            neg +=1
            pol = "neg"
        cursor.execute("INSERT INTO tweets(text, location, created_at, pol_compound, pol) VALUES (%s, %s, %s, %s , %s)", (i['text'],i['user']['location'], date, vs['compound'], pol))


    print("Positive: ", pos, " Negative: ",neg, "Neutral: ", neut)
    panel.commit()



    vs = analyser.polarity_scores(msg)
    print("{:-<65} {}".format(msg, str(vs)))
    print(search_resp.text)


while True:
    pull(cursor, engine)
    time.sleep(2)

