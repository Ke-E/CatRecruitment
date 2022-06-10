create table USE_USER_INFO (
    user_id integer Primary Key,
    name varchar(50) Not Null,
    screen_name varchar(15) Not Null,
    location varchar(30),
    description varchar(160),
    url varchar(100)
);

-- コメント
comment on table USE_USER_INFO is '利用ユーザ情報';
comment on column USE_USER_INFO.user_id is 'ユーザID';
comment on column USE_USER_INFO.name is '名前';
comment on column USE_USER_INFO.screen_name is 'スクリーンネーム';
comment on column USE_USER_INFO.location is '所在地';
comment on column USE_USER_INFO.description is 'プロフィール文';
comment on column USE_USER_INFO.url is 'URL';