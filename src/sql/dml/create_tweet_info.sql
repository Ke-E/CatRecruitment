create table TWEET_INFO (
    tweet_id integer Primary Key,
    tweet_url varchar(100) Not Null,
    text varchar(280) Not Null,
    media_url varchar(60),
    tweet_tm timestamp Not Null
);

-- コメント
comment on table TWEET_INFO is 'ツイート情報';
comment on column TWEET_INFO.tweet_id is 'ツイートID';
comment on column TWEET_INFO.tweet_url is 'ツイートURL';
comment on column TWEET_INFO.text is '本文';
comment on column TWEET_INFO.media_url is '画像URL';
comment on column TWEET_INFO.tweet_tm is '投稿日付';