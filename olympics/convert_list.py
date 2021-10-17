'''
    Author = Shreya Nair
    Link to data file : https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
    
    Program that takes the source csv files and converts them into smaller csv files to be used by tables in the
    database. For olympics assignment.
    Help from : Oliver Calder (CS Lab Assistant)
'''
import csv

athletes_list = []
athlete_awh_list = []
athlete_medal_list = []
games_list = []
event_list = []
sport_list = []

count = 0
reader_noc = csv.reader(open('noc_regions.csv', 'r'))
next(reader_noc)
with open("noc.csv", 'w', newline='') as noc_file:
    noc_writer = csv.writer(noc_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in reader_noc:
        noc_writer.writerow(row)

noc_file.close()

reader = csv.reader(open('athlete_events.csv', 'r'))
next(reader)


for row in reader:

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



    '''
    Building athlete_medal_list entry 
    
        1. if athlete id is not in list of athlete_list then, 
            create a new entry storing id, name, sex
                
        2. if game_name is not in the list of games_list then, 
            create a new entry storing game_id(len of games_list +1), game_name, year, season, city
        
        3. if athlete id and game id is not in list of athlete_awh_list then, 
            create a new entry storing athlete_id, game_id(match ?), age, weight, height 
         
        4. if sport is not in list of sport_list then, 
            create a new sport id (len of sport_list), sport
            
        5. if event is not in list of event_list then,
            create a new entry storing event_id(len of event_list + 1), sport_id( match ?), event_name
        
        6. if athlete_id, game_id, event_id is not in list of athlete_medal_list then, 
            create a new entry storing athlete_id, game_id(match ?), event_id(match ?), noc, team, medal
        
        7. write each list to a csv file for its own table, use csv.writer  
        
    '''
    count += 1
    athlete_found = False
    for list_item in athletes_list:
        if athlete_id in list_item:
            athlete_found = True
            break

    if not athlete_found:
        new_athlete = [athlete_id, name, sex]
        athletes_list.append(new_athlete)

    # Game Table
    game_found = False
    for list_item in games_list:
        if game_name in list_item:
            game_found = True
            game_id = list_item[0]
            break

    if not game_found:
        game_id = len(games_list)
        new_game = [game_id, game_name, year, season, city]
        games_list.append(new_game)


    # AWH
    awh_athlete_found = False
    for list_item in athlete_awh_list:
        if athlete_id == list_item[0] and game_id == list_item[1]:
            awh_athlete_found = True
            break

    if not awh_athlete_found:
        if age == 'NA':
            age = None
        if weight == 'NA':
            weight = None
        if height == 'NA':
            height = None
        new_awh_entry = [athlete_id, game_id, age, weight, height]
        athlete_awh_list.append(new_awh_entry)

    # Sport Table
    sport_found = False

    for list_item in sport_list:
        if sport == list_item[1]:
            sport_found = True
            sport_id = list_item[0]
            break

    if not sport_found:
        sport_id = len(sport_list)
        new_sport = [sport_id, sport]
        sport_list.append(new_sport)


    # Event table
    event_found = False
    for list_item in event_list:
        if event == list_item[2]:
            event_id = list_item[0]
            event_found = True
            break

    if not event_found:
        event_id = len(event_list)
        new_event = [event_id, sport_id, event]
        event_list.append(new_event)

    # Athlete medal table
    if medal == 'NA':
        medal = None # none or empty string ?
    new_medal = [athlete_id, game_id, event_id, noc, team, medal]
    athlete_medal_list.append(new_medal)

    if count % 100 == 0:
        print("Processed ", count, "  lines", end="\r", flush=True)
# Write to my files

with open("athletes.csv", 'w', newline='') as ath_file:
    ath_writer = csv.writer(ath_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for athlete in athletes_list:
        ath_writer.writerow(athlete)

ath_file.close()

with open("athlete_awh.csv", 'w', newline='') as ath_awh_file:
    awh_writer = csv.writer(ath_awh_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for athlete_awh in athlete_awh_list:
        awh_writer.writerow(athlete_awh)

ath_awh_file.close()

with open("games.csv", 'w', newline='') as game_file:
    game_writer = csv.writer(game_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for game in games_list:
        game_writer.writerow(game)

game_file.close()

with open("sports.csv", 'w', newline='') as sport_file:
    sport_writer = csv.writer(sport_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for sport in sport_list:
        sport_writer.writerow(sport)

sport_file.close()

with open("event.csv", 'w', newline='') as event_file:
    event_writer = csv.writer(event_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for event in event_list:
        event_writer.writerow(event)

event_file.close()

with open("athlete_medal.csv", 'w', newline='') as ath_medal_file:
    medal_writer = csv.writer(ath_medal_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for medal in athlete_medal_list:
        medal_writer.writerow(medal)

ath_medal_file.close()

