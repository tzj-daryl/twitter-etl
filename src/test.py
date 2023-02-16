from dotenv import load_dotenv
import os
from twitter_scraper import get_my_timeline, get_tweets_from_user, connect_to_db
import pandas as pd
import sqlalchemy

def main():

    # Load testing environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    # # Test
    # query = """
    #     select *
    #     from dwd_tweet__hi_dev

    # """
    # df=pd.read_sql(sql=query, con=connect_to_db())
    # print(df.head())


    # Test 
    get_tweets_from_user(db_table='dwd_tweet__hi_dev',username='Cointelegraph')



if __name__=='__main__':
    main()