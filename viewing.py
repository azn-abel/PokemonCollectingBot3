from bot import *

from database_management import *
import pokemon
import random
import pickle


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
    embed.add_field(name="PP:", value=f"{collector.poke_points}", inline=True)
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
