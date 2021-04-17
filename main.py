from collections import Counter, defaultdict
import re

class TweetTooLongException(Exception):
    """Exception for tweets longer than 140 characters"""
    def __init__(self, message):
        """Constructor for custom tweet too long exception"""
        super().__init__(message)

class Tweet:
    """Class for each tweet"""
    hashtag_counter = Counter()
    top_tweets = None

    def __init__(self, tweet):
        """
        Contructor tweet
        args:
            tweet(str): text of the tweet
        """
        self.tweet = tweet
        pattern = r"#(\w+)"
        matches = re.finditer(pattern, tweet, re.I)
        for match in matches:
            match = match.group(1).lower()
            Tweet.hashtag_counter[match] += 1

    @staticmethod
    def get_top_tweets():
        """
        Static method for displaying top tweets
        args:
            None
        returns:
            top_10_tweets(dict): dictionary containing top 10 tweets
            {
                'top_tweets': [
                    {
                        'hashtag': 'hashtag text in lowercase",
                        'count': 'count of each hashtag'
                    }
                ]
            }
        """
        Tweet.top_tweets = [(k, v) for k, v in sorted(Tweet.hashtag_counter.items(), key=lambda item: item[1], reverse=True)]
        top_10_tweets = {}
        top_10_tweets['top_tweets'] = []
        for tweet in Tweet.top_tweets[:10]:
            top_10_tweets['top_tweets'].append({'hashtag': "#"+tweet[0], 'count': tweet[1]})
        return top_10_tweets

def exception_handler(func):
    """decorator for handling exceptions"""
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TweetTooLongException as e:
            print(f"{func.__name__} threw TweetTooLongException: {e}")
        except Exception as e:
            print(f"{func.__name__} threw Exception: {e}")
    return inner_function

@exception_handler
def main():
    # reading dummy input from sample_input.txt
    with open("sample_input.txt", "r") as f:
        lines = f.readlines()
        num_of_tweets = int(lines[0].strip())
        i = 0
        for line in lines:
            if i>num_of_tweets:
                break
            dummy_tweet = Tweet(line)
            i += 1

    # taking input from user
    new_tweet_text = input("Please enter new tweet: ")
    while new_tweet_text:
        if len(new_tweet_text)>140:
            raise TweetTooLongException("Tweet is too long")
        else:
            new_tweet = Tweet(new_tweet_text)
        new_tweet_text = input("Enter new tweet to continue (Leave blank to exit): ")

    # getting top 10 tweets
    top10 = Tweet.get_top_tweets()
    for tweet in top10['top_tweets']:
        print("Hashtag: {}; Count: {}".format(tweet['hashtag'], tweet['count']), end="\n")

if __name__=="__main__":
    main()