from bot import *

import pickle
from database_management import *
import pokemon


class Collector:
    instances = []
    instances_dict = {}

    def __init__(self, id):
        self.__class__.instances.append(self)
        self.__class__.instances_dict[id] = self
        self.id = id
        self.pokemon_list = []
        self.unique_list = []
        self.dupe_list = []
        self.poke_points = 0


class Channel:
    instances = []
    instance_dict = {}

    def __init__(self, id, name, server):
        self.__class__.instances.append(self)
        self.__class__.instance_dict[id] = self
        self.id = id
        self.name = name
        self.server = server
        self.drops_enabled = True
        self.drop_active = False
        # print(self.__class__.instances)
        # print(self.__class__.instance_dict)


@client.command()  # FIXED FOR SQL
async def register(ctx):
    author_id = ctx.message.author.id
    for x in Collector.instances:
        if author_id == x.id:
            await ctx.reply("You are already registered to collect!")
            return
    x = Collector(author_id)
    # fileObject = open(f'Collector Data/{x.id}.pickle', 'wb')
    # pickle.dump(x, fileObject)
    # fileObject.close()
    pickle_string = pickle.dumps(x)
    cur.execute("INSERT INTO Collectors (id, instance) VALUES(%s, %s)", (str(author_id), pickle_string,))
    conn.commit()

    await ctx.reply("You are now registered to collect!")
    '''
    y = pickle.load(open(f'Collector Data/{x.id}.pickle', 'rb'))
    print(y.id)
    print(y)
    '''

@client.command()  # FIXED FOR SQL, NEEDS TESTING
async def get(ctx, arg):
    if ctx.message.author.id not in special_privileges:
        await ctx.reply("You dumbass.")
        return

    try:
        # collector = Collector.instances_dict[ctx.message.author.id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(ctx.message.author.id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not a registered collector!")
        return

    poke = arg.lower()
    if poke in pokemon.all_pokemon:
        collector.pokemon_list.append(poke)
        collector.unique_list.append(poke) if str(
            poke) not in collector.unique_list else collector.dupe_list.append(poke)

        # fileObject = open(f'Collector Data/{instance.id}.pickle', 'wb')
        # pickle.dump(instance, fileObject)
        # fileObject.close()

        print(len(collector.unique_list))
        pickle_string = pickle.dumps(collector)

        cur.execute("UPDATE collectors SET instance = %s WHERE id = %s", (pickle_string, str(collector.id)))
        conn.commit()
        await ctx.reply(f"You have acquired {poke.capitalize()}!")
        return
    else:
        await ctx.reply("That is not a valid Pokemon!")
        return
