with both_players as (
  select
  winner_name,
  loser_name
  from stg_matches
), head_to_head as (
  select
    least(winner_name, loser_name) as player_1,
    greatest(winner_name, loser_name) as player_2,
    count(*) as total_matches,
    count(case when winner_name = least(winner_name, loser_name) then 1 end) as player_1_wins,
    count(case when winner_name = greatest(winner_name, loser_name) then 1 end) as player_2_wins
  from both_players
  group by least(winner_name, loser_name), greatest(winner_name, loser_name)
), win_rate as (
  select
  *,
  concat(round(coalesce(player_1_wins, 0) * 100 / coalesce(total_matches, 0), 2), '%') as win_rate_player_1,
  concat(round(coalesce(player_2_wins, 0) * 100 / coalesce(total_matches, 0), 2), '%') as win_rate_player_2
  from head_to_head
)

select * from win_rate