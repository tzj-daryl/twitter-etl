create database if not exists data_mart;

use data_mart;

create table if not exists dwd_tweet__hi (
    username varchar(255),
    name varchar(255),
    user_id bigint,
    tweet_id bigint,
    text varchar(2555),
    created_at datetime
);

grant SELECT, INSERT, DELETE, UPDATE, CREATE, DROP on *.* to 'airflow';

insert into data_mart.dwd_tweet__hi 
values ('@test_username','test_name',0123456789,987654321,"test_tweet",'2023-01-01 15:43:21');

