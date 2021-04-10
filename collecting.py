from bot import *

import pickle
import random
import asyncio
from database_management import conn, cur
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


@client.command()  # NEEDS TO BE FIXED FOR SQL
async def activate(ctx):
    if ctx.message.author.id != 229248090786365443:
        await ctx.reply("You are not authorized to use this command!")
        return
    else:
        for instance in Channel.instances:
            if ctx.channel.id == instance.id:
                if not instance.drops_enabled:
                    instance.drops_enabled = True

                    fileObject = open(f'Channel Data/{instance.id}.pickle', 'wb')
                    pickle.dump(instance, fileObject)
                    fileObject.close()
                    client.loop.create_task(drop_loop(instance.id))
                    await ctx.reply(f"Channel '{ctx.channel}' has been activated for drops!")
                    return
                else:
                    await ctx.reply(f"Channel '{ctx.channel}' is already activated for drops!")
                    return

    x = Channel(ctx.channel.id, str(ctx.channel), str(ctx.message.guild.name))
    fileObject = open(f'Channel Data/{x.id}.pickle', 'wb')
    pickle.dump(x, fileObject)
    fileObject.close()
    client.loop.create_task(drop_loop(x))
    await ctx.reply(f"Channel '{ctx.channel}' has been activated for drops!")


async def drop_loop(instance):
    await client.wait_until_ready()
    # print(instance)
    while True:

        channel = client.get_channel(instance.id)
        embed = discord.Embed(
            title="Pokemon Drop!",
            colour=discord.Colour.red()
        )

        poke = random.choice(pokemon.all_pokemon)

        try:
            temp_file = discord.File(f"Pokemon/images/{poke}.png", filename="image.png")
        except:
            temp_file = discord.File(f"Pokemon/images/{poke}.jpg", filename="image.png")

        embed.add_field(name=f"{pokemon.data.loc[pokemon.data['Name'] == poke, 'Type1'].iloc[0]}",
                        value=poke.capitalize())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="'p!redeem <pokemon-name>' to redeem!")

        wait_time = random.randint(300, 1200)

        print(f"Dropped {poke} in '{instance.name}' in '{instance.server}'. Waiting for {wait_time} seconds.")
        instance.drop_active = True
        instance.drop_pokemon = poke.lower()
        await channel.send(file=temp_file, embed=embed)
        # await ctx.send(channel=channel, embed=embed)
        await asyncio.sleep(wait_time)


@client.command()  # FIXED COLLECTOR PORTION FOR SQL, NEED TO FIX CHANNEL PORTION
async def redeem(ctx, arg):
    channel_id = ctx.channel.id
    drop_channel = Channel.instance_dict[channel_id]
    poke = drop_channel.drop_pokemon.lower()

    # try:
        # collector = Collector.instances_dict[ctx.message.author.id]
    print("got here")
    print(ctx.message.author.id)
    cur.execute("SELECT * FROM collectors WHERE id = %s", (f'{ctx.message.author.id}',))
    retrieved_pickle = cur.fetchone()[1]
    collector = pickle.loads(retrieved_pickle)
    print(retrieved_pickle)
    print(collector)
    # except:
    #     await ctx.reply("You are not a registered collector!")
    #     return

    if drop_channel.drop_active and arg.lower() == poke:
        collector.pokemon_list.append(poke)
        collector.unique_list.append(poke) if str(
            poke) not in collector.unique_list else collector.dupe_list.append(poke)

        # fileObject = open(f'Collector Data/{instance.id}.pickle', 'wb')
        # pickle.dump(instance, fileObject)
        # fileObject.close()

        pickle_string = pickle.dumps(collector)

        cur.execute("UPDATE collectors SET instance = %s WHERE id = %s", (pickle_string, str(collector.id)))
        conn.commit()

        drop_channel.drop_active = False
        drop_channel.drop_pokemon = None
        await ctx.reply(f"Redeemed {poke.capitalize()}!")
        return
    else:
        return
