import os
# DB_HOST = "ec2-3-234-85-177.compute-1.amazonaws.com"
# DB_NAME = "dfjg963os4vl05"
# DB_USER = "onpjrutnbqtplm"
# DB_PASS = "b3f55b9e0432525eba53bc054b4d05998324a697ac7ccf983001f99aed634400"
# DB_HOST = "ec2-54-167-152-185.compute-1.amazonaws.com"
# DB_NAME = "d3vn5oiendgavl"
# DB_USER = "hoozxstnmlnsze"
# DB_PASS = "7be678bf6a9666226e6c23d17d72f5155f3a79ad41ed1f0ee5e464006d1c0861"
if os.getenv('PYCHARM_HOSTED'):
    from environment import *

DB_HOST = os.getenv('DATABASE_URL')[91:133]
DB_NAME = os.getenv('DATABASE_URL')[139:]
DB_USER = os.getenv('DATABASE_URL')[11:25]
DB_PASS = os.getenv('DATABASE_URL')[26:90]

URI = "postgres://hoozxstnmlnsze:7be678bf6a9666226e6c23d17d72f5155f3a79ad41ed1f0ee5e464006d1c0861@ec2-54-167-152-185.compute-1.amazonaws.com:5432/d3vn5oiendgavl"

import os
import pickle

import psycopg2
import psycopg2.extras

from collecting import Collector

# Opening the connection
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

cur.execute("SELECT * FROM collectors")
print(cur.fetchall())
# for filename in os.listdir('Collector Data'):
#     file = open(f'Collector Data/{filename}', 'rb')
#     instance = pickle.load(file)
#     Collector.instances.append(instance)
#     Collector.instances_dict[instance.id] = instance
#     file.close()

# cur.execute("ALTER TABLE Collectors ADD COLUMN id varchar;")
# cur.execute("ALTER TABLE Collectors DROP  name")
# this is a comment

# cur.execute("DELETE FROM Collectors WHERE id is NULL")

# cur.execute("SELECT * FROM collectors WHERE id = %s", (str(229248090786365443),))
# print(cur.fetchone()[1])

# for person in Collector.instances:
#     pickle_string = pickle.dumps(person)
#     cur.execute("INSERT INTO Collectors (id, instance) VALUES(%s, %s)", (str(person.id), pickle_string,))


# Commit Changes
# conn.commit()

# Closing the connection
# cur.close()
# conn.close()
