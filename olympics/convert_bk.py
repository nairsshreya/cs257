'''
    CS 257 Fall 2021
    Shreya Nair

    Program that takes the source csv files and converts them into smaller csv files to be used by tables in the
    database. For olympics assignment.

    Help from : Oliver Calder (CS Lab Assistant)
    links to athletes_events.csv =
'''

import csv


class Athlete:

    def __init__(self, name, sex):
        # self.id = id
        self.name = name
        self.sex = sex
        # self.age = age
        # self.height = height

    def hashable(self):
        return (self.name, self.sex)


class AWH:
    def __init__(self,id, age, weight, height, game_year):
        self.id = id
        self.age = age
        self.height = height
        self.weight = weight
        self.game_year = game_year

    def hashable(self):
        return (self.id, self.age, self.weight, self.height, self.game_year)

class Games:

    def __init__(self, game_year, season, city):
        self.game_year = game_year
        self.season = season
        self.city = city

    def hashable(self):
        return (self.game_year, self.season, self.city)


class NOC:
    def __init__(self, noc_name, region, notes=None):
        self.noc_name = noc_name
        self.region = region
        self.notes = notes


class Medal:
    def __init__(self, noc, medal_type=None):
        self.medal_type = medal_type
        self.noc = noc


athlete_id_list = []
game_id_list = []
noc_id_list = []
games_list = []


# TODO remove redundancy
# def athlete_table(filename):
'''
     Creates a csv file with athlete information per database information
     athlete information being stored in athletes table :
     athlete_id, athlete_name, athlete_sex
'''
debug = False
athletes_dict = {}
reader = csv.reader(open('athlete_events.csv'))
print("opened reader for a")
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
    games = row[8]
    year = row[9]
    season = row[10]
    city = row[11]
    sport = row[12]
    event = row[13]
    medal = row[14]


    new_athlete = Athlete(name, sex)
    athletes_dict[athlete_id] = new_athlete


        if debug:
            print("created ")

        # def games_data(filename):
        '''
            Creates a csv file for the games and season and city
        '''

        games_dict = {}
        reader = csv.reader(open('athlete_events.csv'))
        next(reader)

        for row in reader:
            new_game = Games(row[9], row[10], row[11])
            games_dict[new_game.hashable()] = new_game

        counter = 1
        with open('games.csv', 'w', newline='') as csvfile:
            for game_id in games_dict:
                game_writer = csv.writer(csvfile, delimiter=',')
                temp = games_dict[game_id]
                # write_line = temp.game_year + "," + temp.season + "," + temp.city + "\n"
                game_writer.writerow([counter, game_id])
                counter += 1


        # def athlete_awh_data(filename):
        '''
            Creates a csv file for the athlete age weight and height data
        '''
        athletes_awh = {}
        reader = csv.reader(open('athlete_events.csv'))
        next(reader)
        for row in reader:
            athlete_id = row[0]
            athlete_awh = AWH(row[0], row[3], row[5], row[4], row[8])
            athletes_awh[athlete_awh.hashable()] = athlete_awh

        with open('age_weight_height.csv', 'w', newline='') as csvfile:
            for athlete_id in athletes_awh:
                awh_writer = csv.writer(csvfile, delimiter=',')
                temp = athletes_awh[athlete_id]
                awh_writer.writerow([temp.hashable()])



        # def noc(filename):

        # loading NOC file for NOC table
        new_file4 = open("noc_info.csv", "w")
        counter = 1
        noc_dict = {}
        reader2 = csv.reader(open('noc_regions.csv'))
        next(reader2)
        for row in reader2:
            noc_id = counter
            new_noc = NOC(row[0], row[1], row[2])
            noc_dict[noc_id] = new_noc
            noc_id_list.append(counter)
            counter += 1

        for noc_id in noc_dict:
            temp_noc = noc_dict[noc_id]
            write_line = str(noc_id) + "," + temp_noc.noc_name + ", " + temp_noc.region + ", " + temp_noc.notes + "\n"
            new_file4.write(write_line)


        # medal data
        reader = csv.reader(open('athlete_events.csv'))
        if debug:
            print("At new file 5 for medals")
        next(reader)
        new_file5 = open("medal_data.csv", "w")
        medal = {}
        if debug:
            print("New dictionary for medals")
        reader3 = csv.reader(open("noc_info.csv"))
        for row in reader:
            if debug:
                print("Inside for with reader, row  = ", row)
            a_id_medal = row[0]
            if debug:
                print(a_id_medal)
            for row3 in reader3:
                if debug:
                    print("Inside reader 3 with row ", row3)
                # print(row3)
                # split_row = row3.split(",")
                if row[8] == row3[1]:
                    if debug:
                        print(row[8], " is the noc in the reader, and ", row3[1], "is the noc at row3")
                    noc_medal_id = row3[0]
                    new_medal_entry = Medal(noc_medal_id, row[14])
                    medal[a_id_medal] = new_medal_entry

        for medal_entry in medal:
            temp_medal = medal[medal_entry]
            write_line = a_id_medal + ", " + temp_medal.medal + ", " + temp_medal.noc
            new_file5.write(write_line)

        # new file for linking athlete and the game they played



with open('athletes.csv', 'w', newline='') as csvfile:
    for athlete_id in athletes_dict:
        athlete_writer = csv.writer(csvfile, delimiter=',')
        temp = athletes_dict[athlete_id]
        athlete_writer.writerow([athlete_id, temp])







        # athlete_table('athlete_events.csv')
        # athlete_awh_data('athlete_events.csv')
        # games_data('athlete_events.csv')
