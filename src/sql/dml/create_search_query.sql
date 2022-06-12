create table SEARCH_QUERY (
    query_id integer Not Null,
    query varchar(200) Not Null,
    delete_flg boolean,
    ins_tm timestamp Not Null
);
-- コメント
comment on table SEARCH_QUERY is '検索クエリ';
comment on column SEARCH_QUERY.query_id is 'クエリID';
comment on column SEARCH_QUERY.query is 'クエリ';
comment on column SEARCH_QUERY.delete_flg is '削除フラグ';
comment on column SEARCH_QUERY.ins_tm is '作成日';