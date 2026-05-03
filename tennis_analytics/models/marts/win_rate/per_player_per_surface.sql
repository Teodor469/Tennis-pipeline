with all_players as (
  select
    winner_name as player,
    surface
  from stg_matches
  union all
  select
    loser_name,
    surface
  from stg_matches
), total_matches as (
  select
    player,
    surface,
    count(*) as total_matches
  from all_players
    group by player, surface
), winning_matches as (
  select
    winner_name as player,
    count(*) as total_wins,
    surface
  from stg_matches
  group by winner_name, surface
), last as (
  select 
    player,
    surface,
    concat(round(cast(coalesce(total_wins, 0) as decimal (12,2)) * 100 / coalesce(total_matches, 0), 2), '%') as win_rate
  from total_matches as tm
  left join winning_matches as wm using(player, surface)
)

select * from last