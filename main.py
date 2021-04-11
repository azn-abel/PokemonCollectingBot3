from bot import *

import pickle
import os

import pokemon

VIEWING_ENABLED = True
COLLECTING_ENABLED = True

if COLLECTING_ENABLED:
    from collecting import *

if VIEWING_ENABLED:
    from viewing import *

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

for instance in Channel.instances:
    if instance.drops_enabled:
        client.loop.create_task(drop_loop(instance))

client.loop.create_task(reset_dailies())
client.loop.create_task(change_statuses(pokemon.games_list, 30))
client.run(TOKEN)
