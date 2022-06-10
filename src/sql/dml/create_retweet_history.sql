create table RETWEET_HISTORY (
    tweet_id integer Not Null,
    retweet_tm timestamp Not Null
);
-- コメント
comment on table RETWEET_HISTORY is 'リツイート履歴';
comment on column RETWEET_HISTORY.tweet_id is 'ツイートID';
comment on column RETWEET_HISTORY.retweet_tm is 'リツイート実施日';