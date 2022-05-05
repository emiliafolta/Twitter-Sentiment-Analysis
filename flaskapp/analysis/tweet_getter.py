import tweepy
import time

class tweet_getter:
    def __init__(self, token):
            self.__client = tweepy.Client(bearer_token=token)

    #----private functions----

    def __format_query(self, query):
        
        # Input:    A query to be passed to Twitter's search engine
        # Output:   A modified version of the query that ignores all retweets
        
        if '-is:retweet' in query:
            return query
        else:
            return query + ' -is:retweet'

    def __like_metric(self, tweet_public_metric):
        
        # Input:    tweet_public_metric:    A dictionary of the tweet's public metric returned from the twitter API.
        # Output:   The popularity score of the tweet, here depending entirely on the number of likes that the tweet has
        
        return tweet_public_metric['like_count']

    def __get_next_page(self, query, amount = 100, start = None, end = None, next_page = None):
        
        # Input:    query:      A query to be passed to Twitter's search engine
        #           amount:     Number of tweets to be retrieved (in the range of 1-100 as restricted by Twitter's API)
        #           start:      The earliest date of tweets to be retrieved, must be within the last 7 days, defaults to 7 days ago.
        #           end:        The latest date of tweets to be retrieved, must be within the last 7 days, defaults to current time.
        #           *start and end should be passed as a datetime.datetime object, or a string of the form YYYY-MM-DDTHH:mm:ssZ (i.e. 2009-11-13T10:39:35Z)
        #           next_page:  The pointer to the next_page of the tweets. Can be found in the previous page of tweets returned.
        # Output:   A list of tweets, with information such as id, text, number of likes, retweets, location data and a token to the next page of results.
        
        tweets = self.__client.search_recent_tweets(
            query           = query, 
            tweet_fields    = ['context_annotations', 'created_at', 'geo', 'public_metrics'], 
            place_fields    = ['place_type', 'geo', 'country'], 
            expansions      = ['geo.place_id'],
            start_time      = start,
            end_time        = end,
            max_results     = amount,
            next_token      = next_page)
        return tweets

    def __get_score(self, tweets, metric):
        
        # Input:    tweets:     A list of tweets in the format of being returned by self.__get_next_page (see above)
        #           metric:     A function that takes in two integers (no. of retweets, likes) and returns a score that represents popularity of a tweet
        #           *Higher score is associated with higher popularity.
        # Output:   A list in the form of [(tweet_1.score, tweet_1.id), (tweet_2.score, tweet_2.id)... ]
        
        return [(metric(tweet.public_metrics), tweet.id, tweet.public_metrics) for tweet in tweets.data]

    def __get_popular(self, tweet_scores):

        # Input:    tweet_scores:   A list in the form of [(tweet_1.score, tweet_1.id), (tweet_2.score, tweet_2.id)... ] as returned from __get_score.
        # Output:   A list of the ids of the "top" most popular tweets and their public_metric judging based on the scores in tweet_scores.

        #Feel free to change top to the number of top tweets you want
        top = 3
        top_list = []
        for i in range(top):
            (largest_score, largest_id, largest_public_metric) = max(tweet_scores)
            top_list += [(largest_id, largest_public_metric)]
            tweet_scores.remove((largest_score, largest_id, largest_public_metric))
        return top_list


    def __log_country(self, country, country_count):

        # Input:    country:        A string representing a country as returned by Twitter API
        #           country_count:  A dictionary in the form of {'country_1': x, 'country_2': y... }
        # Output:   None (country_count is updated to increment the count of country by 1.)

        if country not in list(country_count.keys()):
            country_count[country] = 1
        else:
            country_count[country] += 1
        return


    def __update_country(self, tweets, country_count):

        # Input:    tweets:         A list of tweets in the format of being returned by self.__get_next_page (see above)
        #           country_count:  A dictionary in the form of {'country_1': x, 'country_2': y... }
        # Output:   None (country_count is updated to increment the count of each country by the number of times it appears in tweets.)

        if not tweets.includes:
            return

        places = {p["id"]: p for p in tweets.includes['places']}

        for tweet in tweets.data:
            if not tweet.geo:
                continue
            if places[tweet.geo['place_id']]:
                place = places[tweet.geo['place_id']]
                tweet_country = place.country
                if tweet_country != None:
                    self.__log_country(place.country, country_count)
        return

    #----public functions----

    def lookup_tweet_count(self, raw_query, start = None, end = None):

        # Input:    raw_query:  A query to be passed to Twitter's search engine
        #           start:      The earliest date of tweets to be retrieved, must be within the last 7 days, defaults to 7 days ago.
        #           end:        The latest date of tweets to be retrieved, must be within the last 7 days, defaults to current time.
        # Output:   The number of tweets that match the query in the last 7 days.

        query = self.__format_query(raw_query)
        week_count = self.__client.get_recent_tweets_count(query=query, granularity='day', start_time = start, end_time = end)
        return week_count.meta['total_tweet_count']

    def lookup_tweet(self, raw_query, total_amount, start = None, end = None, metric = None):

        # Input:    raw_query:      A query to be passed to Twitter's search engine
        #           total_amount:   The number of tweets to be retrieved
        #           start:          The earliest date of tweets to be retrieved, must be within the last 7 days, defaults to 7 days ago.
        #           end:            The latest date of tweets to be retrieved, must be within the last 7 days, defaults to current time.
        #           metric:         A function that takes in two integers (no. of retweets, likes) and returns a score that represents popularity of a tweet. Defaults to only considering number of likes.
        #           *Higher score is associated with higher popularity.
        # Output:   tweet_storage:  A list of objects, with fields such as id, text, popular_metrics, created_at etc. For more information convert one of the objects to a dictionary with dict() to see it's methods.
        #           *popular_metrics is a dict of the form: {'retweet_count': 9, 'reply_count': 3, 'like_count': 67, 'quote_count': 1}
        #           popular:        The ids and public_metrics of the n tweets that are the most popular. See self.__get_popular above to modify the value of n.
        #           country_count:  A dictionary containing the number of occurences of tweets based in certain countries.

        if total_amount == 0:
            raise ValueError("Number of tweets to be retrieved must be positive")
        
        if metric == None:
            metric = self.__like_metric
        query = self.__format_query(raw_query)
    
        fetched_tweets = 0
        next_page = None
        ran_out_of_tweets = False

        tweet_storage = []
        tweet_scores = []
        country_count = {}

        while fetched_tweets < total_amount and not ran_out_of_tweets:
            fetch_amount = min(total_amount - fetched_tweets, 100)
            
            tweets = self.__get_next_page(query, fetch_amount, start, end, next_page)
            #If no more tweets left break out after this loop iteration
            try:
                next_page = tweets.meta['next_token']
            except:
                ran_out_of_tweets = True

            tweet_storage += tweets.data
            tweet_scores += self.__get_score(tweets, metric)
            self.__update_country(tweets, country_count)

            fetched_tweets += fetch_amount

        #fetch most popular tweets
        popular = self.__get_popular(tweet_scores)

        return tweet_storage, popular, country_count