from dotenv import load_dotenv
import os
from twitter_scraper import get_my_timeline, get_tweets_from_user, connect_to_mysql_db
import pandas as pd
import sqlalchemy

def main():

    # Load testing environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path)

    # Test
    query = """
    select *
    from dwd_tweet__hi
    """
    df=pd.read_sql(sql=query, con=connect_to_mysql_db())
    print(df.head())


    # Test 
    get_my_timeline()



if __name__=='__main__':
    main()