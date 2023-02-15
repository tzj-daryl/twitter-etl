import pandas as pd
from datetime import datetime, timedelta
import pytz
import tweepy
import os
import sqlalchemy


def connect_to_mysql_db():
    # Set the connection parameters
    username = os.getenv('MYSQL_AIRFLOW_USERNAME')
    password = os.getenv('MYSQL_AIRFLOW_PASSWORD')
    host = os.getenv('MYSQL_HOSTNAME')
    port = os.getenv('MYSQL_PORT')
    default_db = os.getenv('MYSQL_DEFAULT_DB')

    try:
        # Connect to the MySQL server
        conn = sqlalchemy.create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{default_db}")
        print('Connected to MySQL Server')

        return conn

    except BaseException as e:
        print(e)


def create_twitter_client():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret_key = os.getenv('CONSUMER_SECRET')
    access_key = os.getenv('ACCESS_KEY')
    access_secret_key = os.getenv('ACCESS_SECRET')
    bearer_token = os.getenv('BEARER_TOKEN')

    # Create API object
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret_key,
        access_token=access_key,
        access_token_secret=access_secret_key,
        return_type=dict,
    )

    return client



def get_my_timeline():
    client = create_twitter_client()

    end = datetime.now(pytz.timezone("Asia/Singapore")).replace(
        microsecond=0, second=0, minute=0
    )
    start = end - timedelta(minutes=60)

    try:
        # Get tweets
        tweets = client.get_home_timeline(
            start_time=start.astimezone(pytz.UTC),
            end_time=end.astimezone(pytz.UTC),
            exclude=["retweets"],
            max_results=100,
            tweet_fields=["created_at", "author_id"],
            expansions="author_id",
        )

        # Convert to df
        if tweets["meta"]["result_count"] > 0:

            df = pd.DataFrame(tweets["data"])
            df = df.astype({"created_at": "datetime64"})
            df["created_at"] = (
                df.created_at.dt.tz_localize("UTC")
                .dt.tz_convert("Asia/Singapore")
                .dt.tz_localize(None)
            )
            df = df.rename({"id": "tweet_id", "author_id": "user_id"}, axis=1)

            usernames_df = pd.DataFrame(tweets["includes"]["users"])  # Get usernames
            usernames_df["username"] = usernames_df.username.apply(lambda x: "@" + x)

            df = df.merge(usernames_df, how="left", left_on="user_id", right_on="id")


            # Insert into MySQL DB
            conn = connect_to_mysql_db()
            table = 'dwd_tweet__hi'
            
            rowsInserted = df[["username", "name", "user_id", "tweet_id", "text", "created_at"]].to_sql(name=table, con=conn, if_exists='append', index=False)
            # .to_csv("data/dwd_timeline__hi_{}.csv".format(start.replace(tzinfo=None).strftime("%Y%m%dT%H")), index=False)

            conn.close()

            print(f"{rowsInserted} rows inserted into {table}")     


        elif tweets["meta"]["result_count"] == 0:
            print(
                "There have been no tweets on your timeline between {} SGT and {} SGT".format(
                    start.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),
                    end.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

    except Exception as err:
        print(f"This is the error message: {err}".format(err))


def get_tweets_from_user(username="CoinDesk"):
    client = create_twitter_client()

    end = datetime.now(pytz.timezone("Asia/Singapore")).replace(
        microsecond=0, second=0, minute=0
    )
    start = end - timedelta(minutes=60)

    try:
        # Get user id
        target_user = client.get_user(username=username)

        # Get tweets
        tweets = client.get_users_tweets(
            id=target_user["data"]["id"],
            start_time=start.astimezone(pytz.UTC),
            end_time=end.astimezone(pytz.UTC),
            exclude=["retweets"],
            # max_results=100,
            tweet_fields=["created_at", "author_id"]
        )

        # Convert to df
        if tweets["meta"]["result_count"] > 0:
            df = pd.DataFrame(tweets["data"])
            df = df.astype({"created_at": "datetime64"})
            df["created_at"] = (
                df.created_at.dt.tz_localize("UTC")
                .dt.tz_convert("Asia/Singapore")
                .dt.tz_localize(None)
            )
            df["username"] = '@' + username
            df['name'] = target_user['data']['name']
            df = df.rename({"id": "tweet_id", "author_id": "user_id"}, axis=1)

            conn = connect_to_mysql_db()
            table = 'dwd_tweet__hi'

            rowsInserted = df[["username", 'name', "user_id", "tweet_id", "text", "created_at"]].to_sql(name=table, con=conn, if_exists='append', index=False)
            # .to_csv("data/dwd_user_tweets__hi_{}.csv".format(start.replace(tzinfo=None).strftime("%Y%m%dT%H")), index=False)

            conn.close()

            print(f"{rowsInserted} rows inserted into {table}")

        elif tweets["meta"]["result_count"] == 0:
            print(
                "There have been no tweets from @{} between {} SGT and {} SGT".format(
                    username,
                    start.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),
                    end.replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

    except Exception as err:
        print(f"This is the error message: {err}".format(err))

