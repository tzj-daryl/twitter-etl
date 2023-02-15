from dotenv import load_dotenv
import os
from twitter_scraper import get_my_timeline, get_tweets_from_user

def main():

    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    get_my_timeline()


if __name__=='__main__':
    main()