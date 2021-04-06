DB_HOST = "ec2-3-234-85-177.compute-1.amazonaws.com"
DB_NAME = "dfjg963os4vl05"
DB_USER = "onpjrutnbqtplm"
DB_PASS = "b3f55b9e0432525eba53bc054b4d05998324a697ac7ccf983001f99aed634400"

import os
import pickle

import psycopg2

from collecting import Collector

# for filename in os.listdir('Collector Data'):
#     file = open(f'Collector Data/{filename}', 'rb')
#     instance = pickle.load(file)
#     Collector.instances.append(instance)
#     Collector.instances_dict[instance.id] = instance
#     file.close()

# Opening the connection
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

# cur.execute("ALTER TABLE Collectors ADD COLUMN id varchar;")
# cur.execute("ALTER TABLE Collectors DROP  name")
# cur.execute("ALTER TABLE Collectors ADD COLUMN instance bytea;")

# cur.execute("DELETE FROM Collectors WHERE id is NULL")

# cur.execute("SELECT * FROM collectors")


# for person in Collector.instances:
#     pickle_string = pickle.dumps(person)
#     cur.execute("INSERT INTO Collectors (id, instance) VALUES(%s, %s)", (str(person.id), pickle_string,))


# Commit Changes
# conn.commit()

# Closing the connection
# cur.close()
# conn.close()
