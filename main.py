# 𝗔𝗦𝗧𝗢𝗟𝗙𝗢 𝗗𝗜𝗦𝗖𝗢𝗥𝗗 𝗕𝗢𝗧 - 𝗦𝗢𝗨𝗥𝗖𝗘
# @author Anime no-Sekai (https://github.com/Animenosekai)
# @author_adaptation dmimukto (https://github.com/dmimukto)
# Based on EasyGif (https://github.com/Animenosekai/EasyGif)


# IMPORTS

### INSTALLED WITH PIP
from discord.ext import commands # to get discord commands
import discord # to communicate with discord
import psutil # to get system details
import requests # to make http requests
from keep_alive import keep_alive

### NATIVE TO PYTHON
import json
import random
import os
import datetime
import asyncio
from collections import Counter
import platform


### REACTION EMOJI WHILE MESSAGE RECEIVED
roger_reaction = '👍'
TOKEN = os.getenv("TOKEN")



def logwrite(msg): #writes chatlog to MESSAGES.log
  with open('GIF_orders.log', 'a+') as f:
    f.write(msg + '\n')
  f.close()


### DEFINING CLIENT/BOT AND ITS PREFIX 
client = commands.Bot(command_prefix='.')

### CLEAR AFTER EVERYTHING IS INITIALIZED
os.system('cls' if os.name == 'nt' else 'clear')


# WHEN THE BOT IS UP
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='.gifhelp')) # BOT ACTIVITY STATUS
    print('Astolfo is ready.') # LOG THAT THE BOT IS READY

# MAIN COMMAND: .gif <SEARCH>
@client.command(pass_context=True)
async def gif(context, *, search):
    await context.message.add_reaction(roger_reaction) # REACT TO SHOW THAT THE BOT HAS UNDESTAND HIS COMMAND

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    print('')
    print("→ '.gif " + search + f"' came from the server: {context.guild}  (user: {context.author})")
    logwrite("→ '.gif " + search + f"' came from the server: {context.guild}  (user: {context.author})") # LOG

    embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gif {}`'.format(search), colour=discord.Colour.blue()) # CREATE AN MESSAGE EMBED INSTANCE

    provider = random.randint(0,1) # CHOOSE THE PROVIDER RANDOMLY

    if provider == 0: #GIPHY
        search.replace(' ', '+') # MAKE SURE THAT SPACES ARE URL-ENCODED
        response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + os.environ['giphy-api-key'] + '&limit=10') # MAKE A SEARCH WITH THE GIPHY API
        data = json.loads(response.text) # GET THE RESPONSE AS A DICT

        gif_choice = random.randint(0, 9) # CHOOSE RANDOMLY FROM THE FIRST 10 ANSWERS
        result_gif = data['data'][gif_choice]['images']['original']['url'] # GETTING THE GIF (result)

        embed.set_image(url=result_gif) # SET THE IMAGE IN THE EMBED AS THE GIF
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy") # SET THE FOOTER WITH THE PROVIDER NAME FOR LEGAL REASONS
        
        await context.send(embed=embed) # SEND THIS NEW MESSAGE
        await context.message.delete() # DELETE THE ORIGINAL MESSAGE (to make it clean)

        print("← '.gif " + search + "' response: " + result_gif)
        logwrite("← '.gif " + search + "' response: " + result_gif) # LOG
        
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": search,
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "giphy",
            "item_number": gif_choice
        }

    elif provider == 1: #TENOR GIF
        search.replace(' ', '+')
        response = requests.get('https://api.tenor.com/v1/search?q=' + search + '&key=' + os.environ['tenor-api-key'] + '&limit=10')
        data = json.loads(response.text)

        gif_choice = random.randint(0, 9)
        result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

        await context.send(embed=embed)
        await context.message.delete()

        print("← '.gif " + search + "' response: " + result_gif)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": search,
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "tenor",
            "item_number": gif_choice
        }
            

# RANDOM GIF: .gifrandom
@client.command(pass_context=True)
async def gifrandom(context):
    await context.message.add_reaction(roger_reaction)

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    print('')
    print(f"→ '.gifrandom' came from the server: {context.guild}  (user: {context.author})")
    embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gifrandom`', colour=discord.Colour.blue())
    provider = random.randint(0,1)
    if provider == 0: #GIPHY RANDOM
        response = requests.get('https://api.giphy.com/v1/gifs/random?api_key=' + os.environ['giphy-api-key'])
        data = json.loads(response.text)
        result_gif = data['data']['images']['original']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")
        await context.send(embed=embed)
        await context.message.delete()
        print("← '.gifrandom' response: " + result_gif)

        # FIREBASE (recording that the user has made a request)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": "random",
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "giphy",
            "item_number": "random"
        }

    elif provider == 1: # TENOR GIF (RANDOM ANIME GIF)
        random_search_key = ['anime', 'manga', 'japan', 'japanese+animation', 'menhera']
        choosing_from_random_search_key = random.randint(0,len(random_search_key) - 1)
        random_search_term = random_search_key[choosing_from_random_search_key]
        response = requests.get('https://api.tenor.com/v1/search?q=' + random_search_term + '&key=' + os.environ['tenor-api-key'] + '&limit=50')
        data = json.loads(response.text)
        gif_choice = random.randint(0, 49)
        result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

        embed.set_image(url=result_gif)
        embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

        await context.send(embed=embed)
        await context.message.delete()

        print("← '.gifrandom' response: " + result_gif)
        
        ### PACKAGING INFOS ABOUT THE REQUEST
        data = {
            "search_term": "random",
            "server": str(context.guild),
            "timestamp": str(current_timestamp),
            "response": result_gif,
            "provider": "tenor",
            "item_number": gif_choice
        }



@client.command(pass_context=True)
async def gifdelete(context):
    await context.message.add_reaction(roger_reaction)
    print('')
    print(f"→ Delete request came from the server: {context.guild}  (user: {context.author})")
    status = await context.send('Searching your last gif...')
    found = False
    messages = await context.channel.history(limit=None).flatten()
    try:
        for message in messages:
            if message.author == client.user:
                if len(message.embeds) != 0:
                    if message.embeds[0].title == f'From {context.author}':
                        await status.edit(content='Deleting it...')
                        found = True
                        await message.delete()
                        print(f"← {context.author}'s GIF deleted on {context.guild}")
                        await status.edit(content='Last gif deleted! ✨')
                        await asyncio.sleep(3)
                        await status.delete()
                        await context.message.delete()
            if found == True:
                break
        if found == False:
            await status.edit(content='❌ An error occured while searching your last gif!')
            await asyncio.sleep(3)
            await status.delete()
            await context.message.delete()
    except:
        await status.edit(content='❌ An error occured while deleting your last gif!')
        await asyncio.sleep(3)
        await status.delete()
        await context.message.delete()



@client.command(pass_context=True)
async def gifchange(context):
    await context.message.add_reaction(roger_reaction)

    now = datetime.datetime.now() # CURRENT TIME AND DATE
    current_timestamp = datetime.datetime.timestamp(now) # GET THE TIMESTAMP FROM THE 'NOW' VARIABLE

    status = await context.send('Searching your last gif...')
    found = False
    messages = await context.channel.history(limit=None).flatten()
    for message in messages:
        if message.author == client.user:
            if len(message.embeds) != 0:

                if message.embeds[0].title == f'From {context.author}':
                    found = True
                    embed_desc = message.embeds[0].description
                    search_term = embed_desc[15:]
                    search_term = search_term[:-1]
                    if search_term == 'ando' or search_term == 'andom' or search_term == 'random':
                        print('')
                        print(f"→ '.gifchange random' came from the server: {context.guild}  (user: {context.author})")
                        embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gifrandom`', colour=discord.Colour.blue())
                        provider = random.randint(0,1)
                        if provider == 0: #GIPHY RANDOM
                            response = requests.get('https://api.giphy.com/v1/gifs/random?api_key=' + os.environ['giphy-api-key'])
                            data = json.loads(response.text)
                            result_gif = data['data']['images']['original']['url']

                            embed.set_image(url=result_gif)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()

                            print("← '.gifchange random' response: " + result_gif)

        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": "random",
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": result_gif,
                                "provider": "giphy",
                                "item_number": "random"
                            }


                        elif provider == 1: # TENOR GIF (RANDOM ANIME GIF)
                            response = requests.get('https://api.tenor.com/v1/search?q=anime&key=' + os.environ['tenor-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            result_gif = data['results'][gif_choice]['media'][0]['gif']['url']

                            embed.set_image(url=result_gif)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()
                            
                            print("← '.gifchange random' response: " + result_gif)

        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": "random",
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": result_gif,
                                "provider": "tenor",
                                "item_number": gif_choice
                            }
                            

                    else:
                        print('')
                        print("→ '.gifchange " + search_term + f"' came from the server: {context.guild}  (user: {context.author})")
                        await status.edit(content='Searching a new gif...')

                        embed = discord.Embed(title='From {}'.format(context.author), description='Command: `.gif {}`'.format(search_term), colour=discord.Colour.blue())
                        provider_from_url = message.embeds[0].image.url
                        provider_from_url = provider_from_url[:19]
                        provider_from_url = provider_from_url[14:]

                        if provider_from_url in "tenor":
                            provider = 0
                        else:
                            provider = 1

                        if provider == 0: #GIPHY
                            search_term.replace(' ', '+')
                            response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search_term + '&api_key=' + os.environ['giphy-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            new_image = data['data'][gif_choice]['images']['original']['url']

                            embed.set_image(url=new_image)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/giphy/giphy-logo.png", text="Powered by Giphy")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()
                            print("← '.gifchange " + search_term + "' response: " + new_image)
                            
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": search_term,
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": new_image,
                                "provider": "giphy",
                                "item_number": gif_choice
                            }
                            

                        elif provider == 1: #TENOR GIF
                            search_term.replace(' ', '+')
                            response = requests.get('https://api.tenor.com/v1/search?q=' + search_term + '&key=' + os.environ['tenor-api-key'] + '&limit=10')
                            data = json.loads(response.text)
                            gif_choice = random.randint(0, 9)
                            new_image = data['results'][gif_choice]['media'][0]['gif']['url']

                            embed.set_image(url=new_image)
                            embed.set_footer(icon_url="https://easygif-assets.netlify.app/assets/public/logos/tenor/tenor-logo.png", text="Powered by Tenor")

                            await message.edit(embed=embed)
                            await status.edit(content='GIF Changed! ✨')
                            await asyncio.sleep(3)
                            await status.delete()
                            await context.message.delete()

                            print("← '.gifchange " + search_term + "' response: " + new_image)
        
                            ### PACKAGING INFOS ABOUT THE REQUEST
                            data = {
                                "search_term": search_term,
                                "server": str(context.guild),
                                "timestamp": str(current_timestamp),
                                "response": new_image,
                                "provider": "tenor",
                                "item_number": gif_choice
                            }
        if found == True:
            break


@client.command(pass_context=True)
async def gifdeletes(context):
    await gifdelete(context)

@client.command(pass_context=True)
async def gifchanges(context):
    await gifchange(context)


@client.command(pass_context=True)
async def gifstats(context):
    await context.message.add_reaction(roger_reaction)
    status = await context.send('Retrieving your informations...')
    print('')
    print(f"→ Stats request came from the server: {context.guild}  (user: {context.author})")

    try:    
        user_node = firebase.child('requests/' + str(context.author.id))
        user_data = user_node.get()
    except:
        await status.edit(content='❌ An error occured while retrieving your infos!')
        await asyncio.sleep(2)
        user_data = "There is an error"

    if user_data != None:
        total_number_of_gifs = len(user_data)
        servers = []
        commands = []
        providers = []
        gifs = []
        for gif in user_data:
            servers.append(user_data[gif]['server'])
            commands.append(user_data[gif]['search_term'])
            providers.append(user_data[gif]['provider'])
            gifs.append(user_data[gif]['response'])
        
        most_used_server = max(set(servers), key=servers.count)
        most_used_search_term = max(set(commands), key=commands.count)
        most_used_provider = max(set(providers), key=providers.count)
        most_used_gif = max(set(gifs), key=gifs.count)
        
        try:
            linkRequest = {"destination": f"{most_used_gif}", "title": "EasyGif - Redirecting you to the orginal GIF"}
            requestHeaders = {"Content-type": "application/json", "apikey": os.environ['rebrandly-api-key']}

            shorten_link_request = requests.post("https://api.rebrandly.com/v1/links", data = json.dumps(linkRequest), headers=requestHeaders)

            shorten_link_information = json.loads(shorten_link_request.text)
            shorten_link = 'https://' + shorten_link_information['shortUrl']
        except:
            print('An error occured while shortening the link')
            shorten_link = most_used_gif
        embed = discord.Embed(title='EasyGif Stats', colour=discord.Colour.blue())
        embed.add_field(name=f'Stats for {context.author.name}', value=f"Total Number of GIFs: **{str(total_number_of_gifs)}**\nMost active server: **{most_used_server}**\nMost searched term: **{most_used_search_term}**\nMost sent GIF: **{shorten_link}**\nMost used GIF provider: **{most_used_provider}**")
        embed.set_footer(text='© Asenturisk 2021')
        await status.edit(content='', embed=embed)
        await context.message.delete()
    elif user_data == "There is an error":
        print(f'Error while retrieving infos for {context.author}')
    else:
        await status.edit(content="You haven't sent any gif with me yet!")
    print(f"← Stats sent on {context.guild} to {context.author}")

@client.command(pass_context=True)
async def gifstat(context):
    await gifstats(context)

@client.command(pass_context=True)
async def gifstats_clear(context):
    await context.message.add_reaction(roger_reaction)
    status = await context.send('Deleting your data...')
    print('')
    print(f"→ User Stats clear request came from the server: {context.guild}  (user: {context.author})")
    await asyncio.sleep(1)
    ### UPDATING THE DATABASE
    #user_node = firebase.child('requests/' + str(context.author.id)) # GETTING THE USER NODE FROM THE DATABASE
    if user_node.get() != None:
        try:
            user_node.delete()
            await status.edit(content='Done! ✨')
            print(f"← Data cleared for {context.author}")
            await asyncio.sleep(2)
            await status.delete()
            await context.message.delete()
        except:
            print('Error while deleting the data')
            await status.edit(content='❌ An error occured while deleting your data!')
            await asyncio.sleep(2)
    else:
        print(f"← No data to clear for {context.author}")
        await status.edit(content="You haven't sent any gif with me yet!")
        await asyncio.sleep(2)

@client.command(pass_context=True)
async def gif_statsclear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstatsclear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstat_clear(context):
    await gifstats_clear(context)

@client.command(pass_context=True)
async def gifstatclear(context):
    await gifstats_clear(context)


@client.command(pass_context=True)
async def gifhelp(context):
    await context.message.add_reaction(roger_reaction)
    print('')
    print(f"→ Help request came from the server: {context.guild}  (user: {context.author})")
    embed = discord.Embed(title='Astolfo Help Center', colour=discord.Colour.blue())
    embed.add_field(name='Available Commands', value="`.gif <search term>`: Searches a GIF on Giphy or Tenor (50% of chance for each) with the term you provided and sends it.\n`.gifrandom`: Sends a random GIF.\n`.gifchange`: Changes your last sent GIF.\n`.gifdelete`: Deletes the last sent GIF.\n`.gifstats`: Gives you your EasyGif's stats.\n`.gifstats_clear`: Clears your data from my database\n`.gifinvite`: Gives you a link to invite EasyGif on any discord server.\n`.easygifstats`: Gives EasyGif bot stats\n`.easygif_dev`: Gives you a link to easygif github repo.\n`.gifhelp`: Sends the message you are currently reading.")
    embed.set_author(name=f"Requested by {context.author}")
    embed.set_footer(text="MuktoDMI, Asenturisk - 2021")
    await context.send(embed=embed)
    print(f"← Help Center sent on {context.guild} to {context.author}")
    await context.message.delete()

@client.command(pass_context=True)
async def gifhelps(context):
    await gifhelp(context)

@client.command(pass_context=True)
async def easygifstats(context):
    await context.message.add_reaction(emoji=roger_reaction)
    print('')
    print(f"→ EasyGif Bot Stats request came from the server: {context.guild}  (user: {context.author})")
    number_of_servers_easygif_is_in = str(len(client.guilds))
    latency = round(client.latency * 1000,2)
    users = str(len(client.users))
    embed = discord.Embed(title='EasyGif Bot Stats', colour=discord.Colour.blue())
    embed.add_field(name='Stats', value=f"Version: **EasyGif v.1.6**\nPing/Latency: **{latency}ms**\nNumber of servers: **{number_of_servers_easygif_is_in}**\nNumber of users: **{users}**\nDeveloper: **MuktoDMI**\nProgramming Language: **Python**")
    embed.add_field(name='Powered by', value="Giphy\nTenor GIF\nReplit\nGoogle Firebase\nRequests Python Library\ndiscord.py Python Library\nRebrand.ly\nNetlify\nGitHub\nDiscord")
    await context.send(embed=embed)
    print(f"← EasyGif Bot Stats sent on {context.guild} to {context.author}")
    await context.message.delete()

@client.command(pass_context=True)
async def easygif_stats(context):
    await easygifstats(context)

@client.command(pass_context=True)
async def easygif_stat(context):
    await easygifstats

@client.command(pass_context=True)
async def easygifstat(context):
    await easygifstats

@client.command(pass_context=True)
async def gifinvite(context):
    print('')
    print(f"→ Invite link request came from the server: {context.guild}  (user: {context.author})")
    await context.message.add_reaction(emoji=roger_reaction)
    await context.send(content="Thank you for choosing to share me with your friends!")
    await asyncio.sleep(2)
    await context.send(content="Here is the link: **https://discord.com/api/oauth2/authorize?client_id="+str(client.user.id)+"&permissions=0&scope=bot**")
    print(f"← Invite link sent on {context.guild} to {context.author}")
    
@client.command(pass_context=True)
async def gifinvites(context):
    await gifinvite(context)



keep_alive()

client.run(TOKEN, bot=True)


