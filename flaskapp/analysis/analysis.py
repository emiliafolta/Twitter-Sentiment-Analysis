import boto3
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tweet_getter as tg

class SentimentAnalysis:
    __comprehend = boto3.client(service_name='comprehend', region_name='eu-west-2')
                
    __token = "AAAAAAAAAAAAAAAAAAAAANm0cAEAAAAAjoKXMxQX%2FwSV2wf4RiFSPeWomQs%3DJfTcDwNVHpMdyL5GunixNf9anfoxQcHaPnUC4CvO9OIbuuP81R"

    def __init__(self, keyword, lang = "en"):
        tweet = tg.tweet_getter(self.__token)
        query = keyword + " lang:" + lang
        self.data = tweet.lookup_tweet(query, 100)[0]

    
    def popular_likes(self):
        sorted_data = sorted(self.data, key = lambda i : i['public_metrics']['like_count'], reverse = True)
        return [sorted_data[0]['text'], sorted_data[1]['text'], sorted_data[2]['text']]
    
    def popular_tweets(self):
        sorted_data = sorted(self.data, key = lambda i : i['public_metrics']['retweet_count'], reverse = True)
        return [sorted_data[0]['text'], sorted_data[1]['text'], sorted_data[2]['text']]
    
    def sentiment_percentage(self):
        no = dict(POSITIVE = 0, NEGATIVE = 0, NEUTRAL = 0, MIXED = 0)
        total = len(self.data)
        for d in self.data:
            text = d['text']
            result = json.loads(json.dumps(self.__comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
            no[result['Sentiment']] += 1
        no['POSITIVE']/=total
        no['NEUTRAL']/=total
        no['NEGATIVE']/=total
        no['MIXED']/=total
        return no 
    
    def sentiment_pie(self):
        percentage = self.sentiment_percentage()
        y = np.array(list(percentage.values()))
        mylabels = np.array(list(percentage.keys()))
        mycolors = np.array(["forestgreen", "Crimson", "AntiqueWhite" , "lightseagreen"])
        
        plt.pie(y, labels = mylabels, autopct='%1.1f%%', colors = mycolors)
        plt.savefig("sentiment_pie.png")
        return plt
    
    def wordcloud(self, w = 800, h = 800, bgcol = 'white', mfsize = 10):
        comment_words = ''
        stopwords = set(STOPWORDS)
        
        for item in self.data:
            text = str(item['text'])
            # split into words
            tokens = text.split()
            # convert to lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
            comment_words += " ".join(tokens)+" "
        
        wdcld = WordCloud(width = w, height = h,
                          background_color = bgcol,
                          stopwords = stopwords,
                          min_font_size = mfsize).generate(comment_words)
        return wdcld.to_image()


instance = SentimentAnalysis("McDonald")
print (instance.popular_likes())
a = instance.sentiment_pie()
print(instance.sentiment_percentage)

