create table USE_HASHTAG_HISTORY (
    tweet_id bigint,
    hashtag varchar(100),
    Primary Key(tweet_id, hashtag)
);

-- コメント
comment on table USE_HASHTAG_HISTORY is '利用ハッシュタグ履歴';
comment on column USE_HASHTAG_HISTORY.tweet_id is 'ツイートID';
comment on column USE_HASHTAG_HISTORY.hashtag is 'ハッシュタグ';