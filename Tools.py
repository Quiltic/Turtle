#this file is literaly just to consolodate resources nothing more


#this is so that the IDE doesent yell at me for not having this in the file. Yes its that annoying
if __name__ == "__main__":
    #import os, subprocess, random, asyncio
    import discord
    from discord.ext import commands
    bot = commands.Bot(";")
    bertle = 0


#all of the needed imports
import asyncio, subprocess
import time, random, os, sys
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except:
    import os
    os.system("python3 -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Weather Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def advanced_weather(location = "cincinnati"):
    """""""""""""""
    Soup stuff
    """""""""""""""
        
    import requests

    if "cincinnati" in location.lower():
        url = ("https://weather.com/weather/hourbyhour/l/229496fea2153559a056b812ded2a50721c9ae6c4a60ff800179cca93ec56caa")
    else:
        #resort to cincinnati if there is no other locaton
        url = ("https://weather.com/weather/hourbyhour/l/229496fea2153559a056b812ded2a50721c9ae6c4a60ff800179cca93ec56caa")
    
    r  = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data)
    #print(soup)

    """""""""""""""
    Get table
    """""""""""""""

    table = soup.find_all('table')[0]
    info = table.find_all('td')

    """""""""""""""
    Get individual data
    """""""""""""""

    time = str(info[1].find_all("span")[0])[23:]#time for aproximate

    description = str(info[2].find_all("span")[0])[6:]#what the wether is outside
    rain_chance = str(info[5].find_all("span")[2])[6:]#%chance for rain
    wind = str(info[7].find_all("span")[0])[15:]# wind (direction speed mph)

    temp_F = str(info[3].find_all("span"))[16:]#temp in F
    temp_F_feals = str(info[4].find_all("span"))[16:]#feels like in F
    humidity = str(info[6].find_all("span")[0])[21:]# % humidity

    """""""""""""""
    Cleanup
    """""""""""""""

    time = time[:time.index('<')]

    description = description[:description.index('<')]
    rain_chance = rain_chance[:rain_chance.index('<')]
    wind = wind[:wind.index('<')]

    temp_F = temp_F[:temp_F.index('<')]
    temp_F_feals = temp_F_feals[:temp_F_feals.index('<')]
    humidity = humidity[:humidity.index('<')]

    """""""""""""""
    Show
    """""""""""""""

    print("Time for estamate:",time)
    print("Weather outside:",description,"   Rain chance:",rain_chance,"   Wind: ",wind)
    print("Tempeture:",temp_F,"   Feels like:",temp_F_feals,"   Humidity:",humidity)
    data = {"Time":time,"Description": description, "Rain": rain_chance, "Wind": wind, "Temp": temp_F, "Feels": temp_F_feals, "Humidity": humidity}

    return(data)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Light Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

async def light_perms(ctx):
    print("working")
    for role in ctx.author.roles:
        print(role)
        if role.name == "Light Wizard":
            #await ctx.send("Glowy!")
            print("Aproved")
            return(True)
    await ctx.send("You dont know magic!")
    return(False)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Tools ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



def rename_file(old_filepath, new_filepath):
    """ Rename a file """
    os.rename(old_filepath, new_filepath)


def getText(file):
    """ Read a file and return the contense """
    with open(file, "r") as f:
        lines = f.read()
        return lines.strip()


async def check_perms(ctx):
    """ This gets weather or not the persion is me (Bertle) """
    print("Checking")
    user = ctx.author.id
    print(bertle,user) #see id of user vs my id
    if bertle == user:
        return(True)
    else:
        print("Cant give acsess to user: %s" % (ctx.author))
        await ctx.send("Sorry pal, but you dont have access.")
        return(False)

        #raise TurtleException('invalid permissions to update',
        #                     'You don\'t got permission to do that, pardner.')
    #else:
    #    raise NotImplementedError()



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#this is to send complex messages and its from old turtle
async def sendmsg(ctx,msg):
    await ctx.send(msg)

#this is for old commands that dont work without it from message event
async def sendmsgorig(message,msg):
    await message.channel.send(msg)

#random number
def randomnum(low,high):
    return random.randrange(low,high+1)


#rolls dice
async def dice(ctx, *args):
    add_on = '0'
    #await sendmsg(ctx, randomnum(1,20))

    #makes it like the origionl input
    message = '[]r ' + str(' '.join(args)).lower()
    print (message)
    
    #splits the data to get the addon
    if "+" in message:
        add_on = message[message.index("+"):]
        message = message[:message.index("+")]
    elif "-" in message:
        add_on = message[message.index("-"):] 
        message = message[:message.index("-")]
    
    # AN IRELIVANT PART!!!
    # rolls 2 d 20 then gives the best
    #if " 2d20" in message:
    #    #await sendmsg(ctx,'d20: %i' % (randomnum(1,20)))
    #    msg = 'd20: %i' % (randomnum(1,20))

    if (message != "[]r +") and (message != "[]r -") and (message != "[]r "):
        numbers = (message.replace("[]r ",''))
        numbers = numbers.replace("d", ' ')
        split = numbers.index(" ")
        
        cur_dice = randomnum(1,int(numbers[split+1:]))
        total = cur_dice
        
        # To stop it from going over discords max chars in a send
        if int(numbers[:split]) < 450:

            #roll X number of dice roles
            msg = 'Dicerolls: %i ' % (cur_dice)
            for a in range(int(numbers[:split])-1):
                cur_dice = randomnum(1,int(numbers[split+1:])) # get the number of dice
                total += cur_dice
                msg = msg + '+ %i ' % (cur_dice) #add the dice to the end of the file

            if add_on != '0':
                total = int(eval(str(total)+add_on))
                msg = msg + add_on[0] + " " + add_on[1:] +"= %i" % (total)
            else:
                msg = msg + "= %i" % (total)
        else:
            #msg = 'grumbel'
            #if the string is longer than discords max char count do the folowing
            await sendmsg(ctx, "Discord doesent like long stuffs so here is the summup.")
            msg = ('Total: %i' % (randomnum(int(numbers[:split]),int(numbers[split+1:])*int(numbers[:split]))))

    else:
        # []r is just a d20
        msg = 'd20: %i' % (randomnum(1,20))
        if add_on != '0':
            msg = msg + ' ' + add_on[0] + " " + add_on[1:] + " = " + str(eval(str(msg[4:]+add_on)))
    

    
    # I dont know why I did this but Im going to keep it for now
    '''
    try:
        if msg == 'grumbel':
            error#just error 
    except:
        await sendmsg(ctx, "Discord doesent like long stuffs so here is the summup.")
        msg = ('Total: %i' % (randomnum(int(numbers[:split]),int(numbers[split+1:])*int(numbers[:split]))))
    '''
    return(msg)






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Sound Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



async def connect_to_channel(channel, vc=None):
    if not channel:
        raise AttributeError('channel cannot be None.')

    if not vc:
        vc = await channel.connect(reconnect=False)

    if vc.channel is not channel:
        await vc.move_to(channel)

    return vc


def get_existing_voice_client(guild):
    for vc in bot.voice_clients:
        if vc.guild is guild:
            return vc