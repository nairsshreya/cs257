Shreya Nair 

Queries from tables 

Olympics project CS 257 Fall 2021


1. SELECT * FROM noc
   ORDER BY noc_id;

2. SELECT DISTINCT athletes.name
   FROM athletes, athlete_medal, noc
   WHERE athletes.id = athlete_medal.athlete_id 
   AND noc.noc_id = athlete_medal.noc_id
   AND noc.noc_id = 'KEN';

3. SELECT athletes.name, athlete_medal.medal, event.event_name, noc.region, games.year
   FROM athletes, athlete_medal, event, noc, games
   WHERE athletes.id = athlete_medal.athlete_id
   AND event.event_id = athlete_medal.event_id
   AND noc.noc_id = athlete_medal.noc_id
   AND games.game_id = athlete_medal.game_id
   AND athletes.name LIKE '%Louganis%'
   ORDER BY games.year;

4. SELECT COUNT (athlete_medal.medal), athlete_medal.noc_id
   FROM athlete_medal, noc
   WHERE noc.noc_id = athlete_medal.noc_id
   AND athlete_medal.medal = 'Gold'
   GROUP BY athlete_medal.noc_id
   ORDER BY COUNT(athlete_medal.medal) DESC;
