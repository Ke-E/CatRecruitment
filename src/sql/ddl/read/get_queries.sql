select
    query_id,
    query
from
    SEARCH_QUERY
where
    delete_flg = false
order by
    query_id