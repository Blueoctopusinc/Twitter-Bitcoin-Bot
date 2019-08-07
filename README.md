# Bitcoin Sentiment Collector
A Twitter bot written in python and deployed on Heroku that queries the [Twitter Standard Search API](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html) to collect tweets referencing BitCoin. 

Sentiment analysis is performed on the message using [VADER-Sentiment-Analysis](https://github.com/cjhutto/vaderSentiment) and the tweets contents, meta-data and analsis stored in a postgreSQL database hosted on [Amazon RDS](https://aws.amazon.com/rds/). 

Primarily written to gather data for an interactive web application.

##Authors
Joshua Yeomans-Gladwin

