import os
import time

if os.getenv('PYCHARM_HOSTED'):
    from environment import *

DB_HOST = os.getenv('DATABASE_URL').split("/")[2].split(":")[1].split("@")[1]
DB_NAME = os.getenv('DATABASE_URL').split("/")[-1]
DB_USER = os.getenv('DATABASE_URL').split("/")[2].split(":")[0]
DB_PASS = os.getenv('DATABASE_URL').split("/")[2].split(":")[1].split("@")[0]



import psycopg2
import psycopg2.extras


# Opening the connection
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()


def cursor_check(cursor):
    global cur
    global conn
    try:
        cursor.execute("SELECT * FROM Collectors")
        print("Cursor check succeeded.")
    except:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        print("Cursor check failed. Refreshing cursor.")








# output_list = []
# for row in cur.fetchall():
#     if row not in output_list:
#         output_list.append(row)
# print(output_list)
# cur.execute("DELETE FROM collectors WHERE id != %s", ("pee",))
# for x in output_list:
#     cur.execute("INSERT INTO Collectors (id, instance) VALUES(%s, %s)", (x[0], x[1],))
# conn.commit()


#     unique_id = row[0]
#     memory = row[1]
#     cur.execute("DELETE FROM collectors WHERE id = %s AND instance != %s", (unique_id, memory))
# conn.commit()
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
