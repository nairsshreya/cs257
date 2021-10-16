Shreya Nair 

Queries from tables 

Olympics project CS 257 Fall 2021


1. SELECT * FROM noc
   ORDER BY noc.noc;

2. SELECT athletes.name
   FROM athletes, athlete_noc, noc
   WHERE athletes.id = athlete_noc.athlete_id 
   AND noc.id = athlete_noc.noc_id
   AND noc.noc = 'KEN';


3. SELECT medal.type, games.year, event.event_type
   FROM athlete_medal, athletes, games, event, athlete_event
   WHERE athlete.id = athlete_medal.athlete_id
   AND athlete.name = 'Greg Louganis'
   ORDER BY games.year;

4. SELECT noc_medal.gold, noc.noc, noc.region
   FROM noc_medal, noc
   WHERE noc.id = noc_medal.noc_id
   ORDER BY noc_medal.gold DESC;
