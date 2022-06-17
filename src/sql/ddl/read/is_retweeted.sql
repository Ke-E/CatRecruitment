select
 exists (
    select
      *
    from
     RETWEET_HISTORY
    where
     tweet_id = %(tweet_id)s
 );