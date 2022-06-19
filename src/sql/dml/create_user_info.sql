create table USER_INFO (
    user_id bigint,
    tweet_id bigint,
    name varchar(50) Not Null,
    screen_name varchar(15) Not Null,
    location varchar(30),
    description varchar(160),
    url varchar(100),
    Primary Key(user_id, tweet_id)
);

-- コメント
comment on table USER_INFO is 'ユーザ情報';
comment on column USER_INFO.user_id is 'ユーザID';
comment on column USER_INFO.tweet_id is 'ツイートID';
comment on column USER_INFO.name is '名前';
comment on column USER_INFO.screen_name is 'スクリーンネーム';
comment on column USER_INFO.location is '所在地';
comment on column USER_INFO.description is 'プロフィール文';
comment on column USER_INFO.url is 'URL';