import argparse
import os

import tweepy
import markovify

import secrets
import news

def create_markov(filename):
  with open(filename) as f:
    data = f.read()
    
  return markovify.NewlineText(data, state_size=3)

def tweet(message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message: {}".format(message))
  api.update_status(status=message)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("num_tweets", type=int,
      help="Number of tweets to publish")
  parser.add_argument("-f", "--news_file", default="news_dataset.txt",
      help="Filename in which news are stored")
  parser.add_argument("-u", "--update", action="store_true", default=False, 
      help="Update news file to recent news from RegistryEvent")
  args = parser.parse_args()
  
  # Update news file if required
  if args.update or not os.path.exists(args.news_file):
    news.update(args.news_file, 20, 2) 

  # Create Markov model
  model = create_markov(args.news_file)
  
  # Tweet
  for i in range(args.num_tweets):
    tweet( model.make_short_sentence(140) )
