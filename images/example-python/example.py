#!/usr/bin/env python

import csv
import json
import sqlalchemy

# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)

# make an ORM object to refer to the table
Example = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)

# # read the CSV data file into the table
# with open('C:/Users/eiti/Downloads/recruitment/data/places.csv') as csv_file:
#   reader = csv.reader(csv_file)
#   next(reader)
#   for row in reader: 
#     connection.execute(Example.insert().values(city = row[0],county=row[1],country=row[2]))

#city,county,country
# # output the table to a JSON file
# with open('C:/Users/eiti/Downloads/recruitment/data/example_python_places.json', 'w') as json_file:
#   rows = connection.execute(sqlalchemy.sql.select([Example])).fetchall()
#   rows = [{'id': row[0], 'city': row[1], 'county': row[2], 'country': row[3]} for row in rows]
#   json.dump(rows, json_file, separators=(',', ':'))

# read the CSV data file into the table
with open('C:/Users/eiti/Downloads/recruitment/data/people.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader:
    a = connection.execute(f"select id from places where city = '{row[3]}'")
    results_as_dict = a.mappings().all()
    print()
    connection.execute(Example.insert().values(given_name = row[0], family_name=row[1], date_of_birth=row[2], place_id=results_as_dict[0]['id']))

# # output the table to a JSON file
# with open('C:/Users/eiti/Downloads/recruitment/data/example_python_people.json', 'w') as json_file:
#   rows = connection.execute(sqlalchemy.sql.select([Example])).fetchall()
#   rows = [{'id': row[0], 'given_name': row[1], 'family_name': row[2], 'date_of_birth': row[3], 'place_of_birth': row[4]} for row in rows]
#   json.dump(rows, json_file, separators=(',', ':'))
