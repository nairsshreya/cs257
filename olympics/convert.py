'''
    Author = Shreya Nair
    Link to data file : https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

    Program that takes the source csv files and converts them into smaller csv files to be used by tables in the
    database. For olympics assignment.
    Help from : Oliver Calder (CS Lab Assistant)
'''

import csv

# Opening and reading the NOCs
reader_noc = csv.reader(open('noc_regions.csv', 'r'))
next(reader_noc)
with open("noc.csv", 'w', newline='') as noc_file:
    noc_writer = csv.writer(noc_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in reader_noc:
        noc_writer.writerow(row)

noc_file.close()

# Opening the general athlete data csv file
reader = csv.reader(open('athlete_events.csv', 'r'))
next(reader)

athletes = {}
ath_awh = {}
games = {}
sports = {}
events = {}
athlete_medal = {}

count = 0
with open("athlete_medal.csv", 'w', newline='') as ath_medal_file:
    medal_writer = csv.writer(ath_medal_file, delimiter=',', quoting=csv.QUOTE_ALL)

    for row in reader:

        count += 1
        athlete_id = row[0]
        name = row[1]
        sex = row[2]
        age = row[3]
        height = row[4]
        weight = row[5]
        team = row[6]
        noc = row[7]
        game_name = row[8]
        year = row[9]
        season = row[10]
        city = row[11]
        sport = row[12]
        event = row[13]
        medal = row[14]

        #Entering data into the athletes file

        if athlete_id not in athletes:
            athlete_data = [athlete_id, name, sex]
            athletes[athlete_id] = athlete_data

        if game_name not in games:
            game_id = len(games)
            game_data = [game_id, game_name, year, season, city]
            games[game_name] = game_data
        else:
            game_id = games[game_name][0]
        awh_id = athlete_id + str(game_id)
        if awh_id not in ath_awh:
            if age == 'NA':
                age = 'NULL'
            if weight == 'NA':
                weight = 'NULL'
            if height == 'NA':
                height = 'NULL'
            awh_data = [athlete_id, game_id, age, weight, height]
            ath_awh[awh_id] = awh_data

        if sport not in sports:
            sport_id = len(sports)
            sports_data = [sport_id, sport]
            sports[sport] = sports_data
        else:
            sport_id = sports[sport][0]

        if event not in events:
            event_id = len(events)
            event_data = [event_id, sport_id, event]
            events[event] = event_data
        else:
            event_id = events[event][0]
        if medal == 'NA':
            medal = 'NULL'
        medal_data = [athlete_id, game_id, event_id, noc, team, medal]
        medal_writer.writerow(medal_data)

        if count % 100 == 0:
            print("Processed ", count, "  lines", end="\r", flush=True)

with open("athletes.csv", 'w', newline='') as ath_file:
    ath_writer = csv.writer(ath_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for athlete, athlete_data in athletes.items():
        ath_writer.writerow(athlete_data)

with open("athlete_awh.csv", 'w', newline='') as ath_awh_file:
    awh_writer = csv.writer(ath_awh_file, delimiter=',', quotechar='"',  quoting=csv.QUOTE_ALL)
    for awh_id, awh_data in ath_awh.items():
        awh_writer.writerow(awh_data)

with open("games.csv", 'w', newline='') as game_file:
    game_writer = csv.writer(game_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for game, game_data in games.items():
        game_writer.writerow(game_data)

with open("sports.csv", 'w', newline='') as sport_file:
    sport_writer = csv.writer(sport_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for sport, sports_data in sports.items():
        sport_writer.writerow(sports_data)
with open("event.csv", 'w', newline='') as event_file:
    event_writer = csv.writer(event_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for event, event_data in events.items():
        event_writer.writerow(event_data)