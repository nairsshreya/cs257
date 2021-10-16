CREATE TABLE athletes (

	id integer,
	name text,
	sex text
);

CREATE TABLE athlete_awh (

	athlete_id integer,
	game_id integer,
	age integer,
	weight integer,
	height integer

);

CREATE TABLE athlete_medal (
	
	athlete_id integer,
	game_id integer,
	event_id integer, 
	noc_id text,
	team text,
	medal text
);

CREATE TABLE noc (

	noc_id text,
	region text,
	notes text

);

CREATE TABLE games (
	
	game_id integer,
	game_name text, 
	year integer,
	season text,
	city text
);

CREATE TABLE sports (

	sport_id integer,
	sport_name text

);

CREATE TABLE event (
	
	event_id integer,
	sport_id integer,
	event_name text
);
