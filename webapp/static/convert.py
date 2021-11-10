'''
    Author: Shreya Nair and Elliot Hanson
    Link to data file : https://www.kaggle.com/nationalparkservice/park-biodiversity?select=species.csv

    Program that takes the source csv files and converts them into smaller csv files to be used by tables in the
    database. For webapp assignment.
'''

import csv

# Opening and reading the parks csv
reader_parks = csv.reader(open('parks_source.csv', 'r'))
parks = {}
next(reader_parks)
with open("parks.csv", 'w', newline='') as parks_file:
    parks_writer = csv.writer(parks_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in reader_parks:
        park_id = row[0]
        park_name = row[1]
        parks[park_name] = park_id
        parks_writer.writerow(row)

parks_file.close()

# Opening the general species data csv file
reader_species = csv.reader(open('species_source.csv', 'r'))
next(reader_species)
species = {}
categories = {}
orders = {}
families = {}
count = 0
with open("species.csv", 'w', newline='') as species_file:
    species_writer = csv.writer(species_file, delimiter=',', quoting=csv.QUOTE_ALL)

    for row in reader_species:

        count += 1
        species_id = row[0]
        park_name = row[1]
        category = row[2]
        order = row[3]
        family = row[4]
        scientific_name = row[5]
        common_names = row[6]
        nativeness = row[9]

        if order == "":
                order = "Unknown"
        if family == "":
                family = "Unknown"
        if nativeness == "":
                nativeness = "Unknown"
                
        #Entering data into the species file
        park_id = parks.get(park_name)
        
        if category not in categories:
            category_id = len(categories)
            categories[category] = category_id
        else:
            category_id = categories[category]

        if order not in orders:
            
            order_id = len(orders)
            orders[order] = order_id
        else:
            order_id = orders[order]
            
        if family not in families:
            family_id = len(families)
            families[family] = family_id
        else:
            family_id = families[family]
        
        species_data = [species_id, park_id, category_id, order_id, family_id, scientific_name, common_names, nativeness]
        species_writer.writerow(species_data)

        if count % 100 == 0:
            print("Processed ", count, "  lines", end="\r", flush=True)
        


with open("categories.csv", 'w', newline='') as categories_file:
    category_writer = csv.writer(categories_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for category in categories:
        category_writer.writerow([categories[category],category])

with open("orders.csv", 'w', newline='') as orders_file:
    order_writer = csv.writer(orders_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for order in orders:
        order_writer.writerow([orders[order],order])
        
with open("families.csv", 'w', newline='') as families_file:
    family_writer = csv.writer(families_file, delimiter=',', quoting=csv.QUOTE_ALL)
    for family in families:
        family_writer.writerow([families[family],family])