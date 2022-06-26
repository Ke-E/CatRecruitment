create table TWEET_INFO (
    tweet_id bigint Primary Key,
    text varchar(280) Not Null,
    tweet_tm timestamp Not Null
);

-- コメント
comment on table TWEET_INFO is 'ツイート情報';
comment on column TWEET_INFO.tweet_id is 'ツイートID';
comment on column TWEET_INFO.text is '本文';
comment on column TWEET_INFO.tweet_tm is '投稿日付';