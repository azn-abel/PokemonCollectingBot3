from bot import *

import pickle
import os
import asyncio
import random
import pandas as pd

import pokemon
from database_management import *

VIEWING_ENABLED = True
COLLECTING_ENABLED = True

if VIEWING_ENABLED:
    from viewing import *

if COLLECTING_ENABLED:
    from collecting import *

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


async def change_statuses(status_list, mins_to_sleep):
    await client.wait_until_ready()
    while True:
        game_name = random.choice(status_list)
        print("changed", game_name)
        await client.change_presence(activity=discord.Game(name=game_name))
        await asyncio.sleep(mins_to_sleep * 60)


@client.command()
async def ping(ctx):
    await ctx.send("pong!")
    await ctx.send(f"```\n{os.environ}\n```")


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

client.loop.create_task(change_statuses(pokemon.games_list, 30))
client.run(TOKEN)
