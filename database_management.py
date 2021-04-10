import os

if os.getenv('PYCHARM_HOSTED'):
    from environment import *

DB_HOST = os.getenv('DATABASE_URL')[91:133]
DB_NAME = os.getenv('DATABASE_URL')[139:]
DB_USER = os.getenv('DATABASE_URL')[11:25]
DB_PASS = os.getenv('DATABASE_URL')[26:90]



import psycopg2
import psycopg2.extras


# Opening the connection
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

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
