import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import got3
import datetime



def friends(name, option, count):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


    info = {}

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': name,'count' : count})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    for i in js['users']:
        info[i["screen_name"]] = i[option]
    return info
print(friends("nba","location",10))

print("\n")

start = str(datetime.datetime(2010, 1, 1))
end = str(datetime.datetime(2017, 1, 27))
def twitts(start_date,end_date,name):
    max_tweets = 10
    tweetCriteria = got3.manager.TweetCriteria().setSince(start_date).setUntil(end_date).setQuerySearch(
        name).setTopTweets(True).setLang('en').setMaxTweets(max_tweets)
    z = []
    for i in range(max_tweets):
        tweet = got3.manager.TweetManager.getTweets(tweetCriteria)[i]
        z.append(tweet.text)
    for i in z:
        print(i, '\n')
    return z
print(twitts(start, end, 'nba'))
