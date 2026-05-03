with dataset as (
  select
    winner_name as winner,
    cast(winner_rank as integer) as winner_rank,
    loser_name as loser,
    cast(loser_rank as integer) as loser_rank,
    tournament_date,
    tourney_level
  from stg_matches
  where winner_rank is not null
  and loser_rank is not null
), percentage as (
  select
    *,
    (winner_rank - loser_rank) as difference,
    cast((difference / winner_rank) * 100 as decimal (12, 2)) as upset_percentage
  from dataset
  where winner_rank > loser_rank
  order by upset_percentage desc
)

select
winner,
winner_rank,
loser,
loser_rank,
concat(cast(upset_percentage as string), '%') as upset_percentage,
tournament_date,
tourney_level
from percentage

