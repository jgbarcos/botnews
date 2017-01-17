# BotNews

Twitter bot that creates headlines based on recent news.

### Details

News are gathered from [EventRegistry](https://eventregistry.org/). Firts it queries trending concepts and then gathers news titles about those concepts to create a dataset of news titles.

Then it creates a Markov Chain model to generate the headlines that are going to be tweeted.

### Prerequisites
```
pip install tweepy markovify eventregistry
```

### Usage

Create secrets.py by filling the fields of TEMPLATE-secrets.py

Then execute bot.py like:
```
bot.py 5 -u -f news_dataset.txt
```

This would publish 5 tweets after updating (-u) the news dataset file (-f).

Check help by passing -h or --help to bot.py.
