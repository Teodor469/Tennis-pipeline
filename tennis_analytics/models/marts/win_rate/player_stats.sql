WITH player_wins AS (
    SELECT winner_name as player, COUNT(*) as wins
    FROM stg_matches
    GROUP BY winner_name
), player_loses as (
  select loser_name as player,
  count(*) as losses
  from stg_matches
  group by loser_name
), win_rate as (
select
  coalesce(w.player, l.player) as player_name,
  coalesce(w.wins, 0) as wins,
  coalesce(l.losses, 0) as losses,
  coalesce(w.wins, 0) + coalesce(l.losses, 0) as total_matches,
  concat(ROUND(COALESCE(w.wins, 0) * 100.0 / (COALESCE(w.wins, 0) + COALESCE(l.losses, 0)), 2), '%') as win_rate
  from player_wins as w
  full outer join player_loses as l
  on w.player = l.player
  order by total_matches
)
SELECT * FROM win_rate where total_matches >= 10