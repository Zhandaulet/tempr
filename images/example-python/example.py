#!/usr/bin/env python

import csv
# from distutils.log import error
import json
import sqlalchemy
import collections
from datetime import date, datetime

#defining new function json_serial
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)

try: 
  connection.execute("""create table if not exists `places` ( 
    `id` int not null auto_increment,
    `city` varchar(20) DEFAULT NULL,
    `county` varchar(20) DEFAULT NULL,
    `country` varchar(20) DEFAULT NULL,
    PRIMARY KEY (`id`)
  );""")
except RuntimeError:
  print(RuntimeError)

print("creation of places completed!")

try:
  connection.execute("""create table if not exists `people` (
    `id_people` int not null auto_increment,
    `given_name` varchar(80) default null,
    `family_name` varchar(80) default null,
    `date_of_birth` date default null,
    `place_id` int null,
    INDEX `idx_place_id` (`place_id`),
    FOREIGN KEY (`place_id`)
    REFERENCES `places`(`id`)
    on DELETE CASCADE,
    primary key (`id_people`)
  );""")
except RuntimeError:
  print(RuntimeError)


print("creation of people completed!")


try:
  connection.execute('SET FOREIGN_KEY_CHECKS = 0; TRUNCATE TABLE people; TRUNCATE TABLE places; SET FOREIGN_KEY_CHECKS = 1;')
except RuntimeError:
  print(RuntimeError)

print("truncated tables!")

# make an ORM object to refer to the table
ex_places = sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)

# read the CSV data file into the table
with open('/data/places.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader: 
    connection.execute(ex_places.insert().values(city = row[0],county=row[1],country=row[2]))

print("places csv has been loaded to places table!")

# output the table to a JSON file
with open('/data/example_python_places.json', 'w') as json_file:
  rows = connection.execute(sqlalchemy.sql.select([ex_places])).fetchall()
  rows = [{'id': row[0], 'city': row[1], 'county': row[2], 'country': row[3]} for row in rows]
  json.dump(rows, json_file, separators=(',', ':'))

print("json file for places has been created!")

# make an ORM object to refer to the table
ex_people = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)


# read the People CSV data file into the table
with open('/data/people.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader:
    a = connection.execute(f"select id from places where city = '{row[3]}'")
    results_as_dict = a.mappings().all()
    connection.execute(ex_people.insert().values(given_name = row[0], family_name=row[1], date_of_birth=row[2], place_id=results_as_dict[0]['id']))

print("people data is inserted to people table!")

# output the table to a JSON file
with open('/data/people_output.js',"w") as json_file:
  rows = connection.execute(sqlalchemy.sql.select([ex_people])).fetchall()

  rows = [{'id_people': row[0], 'given_name': row[1], 'family_name': row[2], 'date_of_birth': row[3], 'place_id': row[4]} for row in rows]
  json.dump(rows, json_file, separators=(',', ':'), default=json_serial)

print("json file for people has been extracted!")
  
# output the compare_output file

sql_stat = "select places.country, count(places.country) as count_country  from people as p join places as places on places.id = p.place_id group by places.country;"
compare_rows = connection.execute(sql_stat).fetchall()
  
rowarraytolist = {}

for eachrow in compare_rows:
    rowarraytolist[eachrow[0]] = eachrow[1]

print(rowarraytolist)
j = json.dumps(rowarraytolist,default=json_serial)

with open('/data/compare_output.json', 'w') as json_file:
  json_file.write(j)    

print("compare data extracted!")