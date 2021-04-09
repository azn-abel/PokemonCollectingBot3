import discord
from discord.ext import commands
import pickle
import os
import asyncio
import random
import pandas as pd

from collecting import Collector, Channel
import pokemon
from database_management import *

if os.getenv('PYCHARM_HOSTED'):
    from environment import *

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=['p!', 'P!'], intents=intents)

special_privileges = [229248090786365443]


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


'''
---------------- FOR VIEWING -----------------
'''


@client.command(aliases=['collection', 'col'])
async def _collection(ctx, *args):
    author = ctx.message.author
    pfp = author.avatar_url
    output_list = []
    output_string = ""
    collection_embed = discord.Embed(
        title=f"{str(ctx.author)[:-5]}'s collection:"
    )
    collection_embed.set_thumbnail(url=pfp)

    collector_id = ctx.message.author.id
    try:
        # collector = Collector.instances_dict[collector_id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(collector_id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not registered to collect!")
        return

    for poke in collector.pokemon_list:
        output_list.append(poke.capitalize())
        output_list.sort()

    total_page_nums = pokemon.getPageNums(output_list)

    if not args:
        page_num = 1
    else:
        if int(args[0]) > total_page_nums or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = args[0]

    indices = pokemon.getIndices(total_page_nums, page_num)

    collection_embed.set_footer(text=f"Viewing page {page_num} of {total_page_nums}.")

    for output in output_list[indices[0]:indices[1]]:
        output_string += f"- {output}\n"
    collection_embed.add_field(name="Pokemon:",
                               value=output_string if output_string != "" else "You don't have any Pokemon!")
    await ctx.send(embed=collection_embed)
    return


@client.command()
async def dupes(ctx, *args):
    author = ctx.message.author
    pfp = author.avatar_url
    output_list = []
    output_string = ""
    collection_embed = discord.Embed(
        title=f"{str(ctx.author)[:-5]}'s Dupes:"
    )
    collection_embed.set_thumbnail(url=pfp)

    collector_id = ctx.message.author.id
    try:
        # collector = Collector.instances_dict[collector_id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(collector_id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not registered to collect!")
        return

    for poke in collector.dupe_list:
        output_list.append(poke.capitalize())
        output_list.sort()

    total_page_nums = pokemon.getPageNums(output_list)

    if not args:
        page_num = 1
    else:
        if int(args[0]) > total_page_nums or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = args[0]

    indices = pokemon.getIndices(total_page_nums, page_num)

    collection_embed.set_footer(text=f"Viewing page {page_num} of {total_page_nums}.")

    for output in output_list[indices[0]:indices[1]]:
        output_string += f"- {output}\n"
    collection_embed.add_field(name="Pokemon:",
                               value=output_string if output_string != "" else "You don't have any Dupes!")
    await ctx.send(embed=collection_embed)
    return


@client.command()
async def unique(ctx, *args):
    author = ctx.message.author
    pfp = author.avatar_url
    output_list = []
    output_string = ""
    collection_embed = discord.Embed(
        title=f"{str(ctx.author)[:-5]}'s Unique Pokemon:"
    )
    collection_embed.set_thumbnail(url=pfp)
    collector_id = ctx.message.author.id
    try:
        # collector = Collector.instances_dict[collector_id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(collector_id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not registered to collect!")
        return

    for poke in collector.unique_list:
        output_list.append(poke.capitalize())
        output_list.sort()

    total_page_nums = pokemon.getPageNums(output_list)

    if not args:
        page_num = 1
    else:
        if int(args[0]) > total_page_nums or int(args[0]) < 1:
            page_num = 1
        else:
            page_num = args[0]

    indices = pokemon.getIndices(total_page_nums, page_num)

    collection_embed.set_footer(text=f"Viewing page {page_num} of {total_page_nums}.")

    for output in output_list[indices[0]:indices[1]]:
        output_string += f"- {output}\n"
    collection_embed.add_field(name="Pokemon:",
                               value=output_string if output_string != "" else "You don't have any Pokemon!")
    await ctx.send(embed=collection_embed)
    return


@client.command()
async def roll(ctx):
    embed = discord.Embed(
        title="Rolled Pokemon"
    )

    poke = random.choice(pokemon.all_pokemon)

    try:
        temp_file = discord.File(f"Pokemon/images/{poke}.png", filename="image.png")
    except:
        temp_file = discord.File(f"Pokemon/images/{poke}.jpg", filename="image.png")

    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=f"You rolled {poke.capitalize()}!")

    await ctx.reply(file=temp_file, embed=embed)


@client.command()
async def view(ctx, pokemon):
    try:
        # collector = Collector.instances_dict[collector_id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(ctx.message.author.id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not registered to collect!")
        return

    try:
        temp_file = discord.File(f"Pokemon/images/{pokemon.lower()}.png", filename="image.png")
    except:
        try:
            temp_file = discord.File(f"Pokemon/images/{pokemon.lower()}.jpg", filename="image.png")
        except:
            await ctx.reply("That is not a valid Pokemon!")
            return

    if pokemon.lower() not in collector.pokemon_list:
        await ctx.reply("You do not own this Pokemon!")
        return

    embed = discord.Embed(
        title="Viewing Pokemon"
    )

    embed.set_image(url="attachment://image.png")
    embed.set_footer(text=f"Viewing {pokemon.capitalize()}!")

    await ctx.reply(file=temp_file, embed=embed)


@client.command()
async def stats(ctx):
    author = str(ctx.message.author)
    try:
        # collector = Collector.instances_dict[ctx.message.author.id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(ctx.message.author.id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not a registered collector!")
        return

    embed = discord.Embed(
        title="Pokemon Collection Stats"
    )
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.set_footer(text="Use command p!collection to view a full list")
    embed.add_field(name="User", value=f"{ctx.message.author.mention}", inline=False)
    embed.add_field(name="Collection:", value='** **', inline=False)

    counter = 0
    for type in pokemon.types:
        pokecount = 0
        for poke in collector.unique_list:
            if f"{pokemon.data.loc[pokemon.data['Name'] == poke, 'Type1'].iloc[0]}" == type:
                pokecount += 1

        embed.add_field(name=type, value=f"{pokecount}/{pokemon.counts[type]}",
                        inline=False if counter % 3 == 0 and counter != 0 else True)

    embed.add_field(name="Total:", value=f"**{len(collector.unique_list)}/{len(pokemon.all_pokemon)}**")

    await ctx.send(embed=embed)


'''
@client.command()
async def drop(ctx):
    embed = discord.Embed(
        title="Pokemon Drop!"
    )

    poke = random.choice(pokemon.all_pokemon)

    try:
        temp_file = discord.File(f"Pokemon/images/{poke}.png", filename="image.png")
    except:
        temp_file = discord.File(f"Pokemon/images/{poke}.jpg", filename="image.png")

    embed.add_field(name=f"{pokemon.data.loc[pokemon.data['Name'] == poke, 'Type1'].iloc[0]}", value=poke.capitalize())
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text="'p!redeem <pokemon-name>' to redeem!")

    await ctx.send(file=temp_file, embed=embed)
'''

'''
---------------- FOR DROPS -----------------
'''


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

    try:
        # collector = Collector.instances_dict[ctx.message.author.id]
        cur.execute("SELECT * FROM collectors WHERE id = %s;", (str(ctx.message.author.id),))
        retrieved_pickle = cur.fetchone()[1]
        collector = pickle.loads(retrieved_pickle)
    except:
        await ctx.reply("You are not a registered collector!")
        return

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


@client.command()
async def ping(ctx):
    await ctx.send("pong!")
    await ctx.send(str(os.environ))


@client.command(name='69')
async def _69(ctx):
    for emoji in ['\N{REGIONAL INDICATOR SYMBOL LETTER N}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                  '\N{REGIONAL INDICATOR SYMBOL LETTER E}']:
        await ctx.message.add_reaction(emoji)


for filename in os.listdir('Collector Data'):
    file = open(f'Collector Data/{filename}', 'rb')
    instance = pickle.load(file)
    Collector.instances.append(instance)
    Collector.instances_dict[instance.id] = instance
    file.close()

for filename in os.listdir('Channel Data'):
    file = open(f'Channel Data/{filename}', 'rb')
    instance = pickle.load(file)
    Channel.instances.append(instance)
    Channel.instance_dict[instance.id] = instance
    file.close()

print(Collector.instances)
for instance in Collector.instances:
    print(instance.id)
    print(f"All: {instance.pokemon_list}")
    print(f"Unique: {instance.unique_list}")
    print(f"Dupes: {instance.dupe_list}")

for instance in Channel.instances:
    if instance.drops_enabled:
        client.loop.create_task(drop_loop(instance))

client.run(TOKEN)
