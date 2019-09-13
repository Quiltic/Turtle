import asyncio, subprocess
import time, random, os, sys

from wether import *

try:
    import discord
    from discord.ext import commands
except:
    os.system("python3 -m pip install discord.py")
    import discord
    from discord.ext import commands

#from pydub import AudioSegment
#from guild_info import GuildInfo

#from help import helpEmbed, get_list_embed, make_sounds_dict, get_rand_activity

#tts_path = 'resources/voice.exe'

prefix = '[]'
bot = commands.Bot(prefix)#, connector=aiohttp.TCPConnector(ssl=False)
currStatus = discord.Activity(name="turtle sounds. | []help", type=discord.ActivityType.listening)

#get home directory
cwd = os.getcwd()

bertle = 275002179763306517 #my id  #bot.get_user(bot.owner_id)
cur_user = 0

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@bot.command()
async def showTerminal(ctx, *args):
    cmd = []
    for a in args:
        cmd.append(a)
    print(cmd)

    if await check_perms(ctx):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
        #output = pipe.read()
        words = "```"
        for out in output:
            out = out.split("\n")
            for ou in out:
                words = words + ou + "\n"
            
        words = words + "```"
        await ctx.send(words)
        

@bot.command()
async def update(ctx):
    """This updates Turtle to the latest version of itself from github. BERTLE ONLY"""
    if await check_perms(ctx):
        await sendmsg(ctx,"Updating")
        print("On")
        print(cwd)
        #go home you lazy bumb
        os.system(("cd "+ cwd))

        await sendmsg(ctx,"Directory changed")
        print("changed cd")
        #open update
        callfreind = "python3 /home/pi/Turtle/TurtleUpdate.py &"
        print(callfreind)
        os.system(callfreind)
        #subprocess.Popen(callfreind)

        await sendmsg(ctx,"Opened Friend!")
        print("Summoned!")
        
        #turn off
        await turnoff(ctx)


#this uploads turtle to github if enabled.
@bot.command()
async def upload(ctx):
    """This uploads the current version of Turtle to github. BERTLE ONLY"""
    if await check_perms(ctx):
        os.system(("cd "+ cwd))
        os.system("git add .")
        time.sleep(1)
        os.system("git commit -m Turtle pushed me.")
        time.sleep(3)
        os.system("git push")


@bot.command()
async def ipadress(ctx):
    """This gives the current IP for the PI that it is running on. BERTLE ONLY"""
    if await check_perms(ctx):
        #Yoinked from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/24564613#24564613
        if os.name != "nt":
            import fcntl #this only works on luinex dont know why
            import struct
            def get_interface_ip(ifname):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                        s.fileno(),
                        0x8915,  # SIOCGIFADDR
                        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
                        # Python 2.7: remove the second argument for the bytes call
                    )[20:24])

        import socket
        IPAddr = socket.gethostbyname(socket.gethostname())
        if IPAddr.startswith("127.") and os.name != "nt":
            interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            for ifname in interfaces:
                try:
                    IPAddr = get_interface_ip(ifname)
                    break
                except IOError:
                    pass    

        await ctx.send(IPAddr)




def rename_file(old_filepath, new_filepath):
    os.rename(old_filepath, new_filepath)


def getText(file):
    with open(file, "r") as f:
        lines = f.read()
        return lines.strip()


async def check_perms(ctx):
    print("Checking")
    user = ctx.author.id
    print(bertle,user) #see id of user vs my id
    if bertle == user:
        return(True)
    else:
        print("Cant give acsess to user: %s" % (ctx.author))
        await ctx.send("Sorry, but you dont have access to that.")
        return(False)

        #raise TurtleException('invalid permissions to update',
        #                     'You don\'t got permission to do that, pardner.')
    #else:
    #    raise NotImplementedError()




"""
#redo
def delete_file(file, guild):
    path = guilds[guild.id].sound_folder
    os.remove(sound)
"""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@bot.command()
async def timmer(ctx, delay = 5):
    """Makes me set a timemer for # then 🐢"""
    await ctx.send(("Counting down from: %s" % (delay)))
    await asyncio.sleep(delay)
    await ctx.send("Times up!")
    await ctx.message.add_reaction("🐢")


@bot.command()
async def weather(ctx):
    await ctx.message.add_reaction("🐢")
    data = advanced_weather()
    msg = "Currently: " + data["Description"]
    timestuff = "Around: "+ data["Time"]
    forcast=discord.Embed(title=timestuff, description=msg, color=0x1c57e3)
    forcast.set_author(name="Turtle's Forecast") #icon_url="Tertle.png" 
    #forcast.set_thumbnail(url="Tertle.png")
    forcast.add_field(name="Current Tempterture (F):", value=data["Temp"], inline=True)
    forcast.add_field(name="Feels like Tempterture (F):", value=data["Feels"], inline=True)
    forcast.add_field(name="Humidity: ", value=data["Humidity"], inline=True)

    forcast.add_field(name="Rain chance in %:", value=data["Rain"], inline=True)
    forcast.add_field(name="Wind: ", value=data["Wind"], inline=True)
    await ctx.send(embed = forcast)



@bot.command()
async def turtle(ctx):
    """Makes me react with 🐢"""
    await ctx.message.add_reaction("🐢")

@bot.command()
async def r(ctx, *args):
    """This rolls a # of dice and gives the output. Usage: []r 1d4 +4"""
    stuff = await dice(ctx, *args)
    await sendmsg(ctx,stuff)

@bot.command()
async def Yell(ctx):
    """Turtle just Yells at you"""
    await sendmsg(ctx,"AGGGG")

@bot.command()
async def GitURL(ctx):
    """This gives the git repository on github."""
    await ctx.send("My repository is: https://github.com/Quiltic/Turtle.git")








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
    addon = '0'
    #await sendmsg(ctx, randomnum(1,20))

    message = '[]r ' + str(' '.join(args)).lower()
    print (message)
    
    
    if "+" in message:
        addon = message[message.index("+"):]
        message = message[:message.index("+")]
    elif "-" in message:
        addon = message[message.index("-"):]
        message = message[:message.index("-")]
    
    if " 2d20" in message:
        #await sendmsg(ctx,'d20: %i' % (randomnum(1,20)))
        msg = 'd20: %i' % (randomnum(1,20))

    elif (message != "[]r +") and (message != "[]r -") and (message != "[]r "):
        numbers = (message.replace("[]r ",''))
        numbers = numbers.replace("d", ' ')
        split = numbers.index(" ")
        
        curdice = randomnum(1,int(numbers[split+1:]))
        total = curdice
        
        if int(numbers[:split]) < 450:
            msg = 'Dicerolls: %i ' % (curdice)
            for a in range(int(numbers[:split])-1):
                curdice = randomnum(1,int(numbers[split+1:]))
                total += curdice
                msg = msg + '+ %i ' % (curdice)
            if (addon != '0'):
                total = int(eval(str(total)+addon))
            if addon != '0':
                msg = msg + addon[0] + " " + addon[1:] +"= %i" % (total)
            else:
                msg = msg + "= %i" % (total)
        else:
            msg = 'grumbel'

    else:
        msg = 'd20: %i' % (randomnum(1,20))
        if addon != '0':
            msg = msg + ' ' + addon[0] + " " + addon[1:] + " = " + str(eval(str(msg[4:]+addon)))
    try:
        if msg == 'grumbel':
            error#just error 
    except:
        await sendmsg(ctx, "Discord doesent like long stuffs so here is the summup.")
        msg = ('Total: %i' % (randomnum(int(numbers[:split]),int(numbers[split+1:])*int(numbers[:split]))))
    
    return(msg)






#this is from old turtle but i still love it
async def conversate(message):
    global cur_user

    if "make me a sandwich" in message.content.lower(): # simple ping
        await sendmsgorig(message, "Here you go!")
        await message.channel.send(file=discord.File('Sandwich.jpg'))

    elif "bubble" in message.content.lower(): # simple ping
        await sendmsgorig(message, "BUBBLES!")

    elif "random" == message.content.lower():
        await sendmsgorig(message, "RANDOM NUMBERS YOU SAY!?")
        for a in range(randomnum(2,24)):
            await sendmsgorig(message,randomnum(10,10000))
        await sendmsgorig(message, "Fin.")

    elif "what time is it" in message.content.lower():
        await sendmsgorig(message, "TURTLE TIME!")
        msg = "🐢"
        for a in range(randomnum(2,24)):
            msg = msg + "🐢"
        await sendmsgorig(message, msg)

    elif "i need an army" in message.content.lower():
        await sendmsgorig(message, "On it boss!")
        msg = "🐢"
        rand = randomnum(100,200)
        for a in range(rand):
            msg = msg + "🐢"
        await sendmsgorig(message, msg)
        msg = "I was able to get " + str(rand) + " Turtles for the cause!"
        await sendmsgorig(message, msg)

    elif "yell at " in message.content.lower():
        msg = ("They arnt here, sorry %s." % (message.author.name))
        for users in bot.users:
            for b in message.guild.members:
                if b == users:
                    if message.content.lower()[8:] in users.name.lower():
                        msg = "Hey <@%s>! %s wants you." % (users.id,message.author.name)
        await sendmsgorig(message, msg)

    elif "help" in message.content.lower():
        await sendmsgorig(message, "I can yell at someone, make a sandwich, I like bubbles, and randomness..., help rase an army, get the time")
        await sendmsgorig(message, "Helpful?")
    elif "hi" in message.content.lower(): # simple ping
        await sendmsgorig(message, "Hello!")
    else:# simple ping
        await sendmsgorig(message, "Ok then!") 
    
    cur_user = 0

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Sound Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


async def connect_to_user(ctx):
    try:
        vc = ctx.voice_client
        user_channel = ctx.author.voice.channel
        return await connect_to_channel(user_channel, vc)
    except:
        raise TurtleException('User was not in a voice channel.',
                             msg='Get in a voice channel!')


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

#Join the voice channel
@bot.command()
async def join(ctx):
    """Joins me to the users call/channel."""
    _ = await connect_to_user(ctx)

#leave the voice channel
@bot.command()
async def leave(ctx):
    """Makes me leave the call/channel."""
    if ctx.voice_client and ctx.voice_client.is_connected():
        #loc = os.path.join('resources', 'soundclips', 'leave')
        #sounds = make_sounds_dict(loc)
        #soundname = random.choice(list(sounds.values()))
        #sound = os.path.join(loc, soundname)
        #play_sound_file(sound, ctx.voice_client)
        time.sleep(1)
        await ctx.guild.voice_client.disconnect()



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
######################  This and Main Stuff was taken from Ben Rucker it has been modifyed ######################
                         https://github.com/benrucker
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Turn off
@bot.command()
async def perish(ctx):
    """Force turns me off. BERTLE ONLY"""
    if await check_perms(ctx):
        await sendmsg(ctx,"Im off now.")
        print("Bye!")
        await bot.close()

#Turn off for the bot to use when updating
async def turnoff(ctx):
    await sendmsg(ctx,"Restarting?")
    print("Bye!")
    await bot.close()

@bot.event
async def on_command_error(ctx, e):
    if type(e) is commands.errors.CommandInvokeError:
        e = e.original
        if type(e) is TurtleException:
            print('Caught TurtleException: ' + str(e))
            await ctx.send(e.message)
    else:
        raise e




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
######################  Main Stuff  ######################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



@bot.event
async def on_ready():
    global guilds
    await bot.change_presence(activity=currStatus)

    #guilds = dict()
    #for guild in bot.guilds:
    #    guilds[guild.id] = GuildInfo(guild)

    #print(f'Logged into {str(len(guilds))} guilds:')
    #for guild in list(guilds.values()):
    #    print(f'\t{guild.name}:{guild.id}')
    print("Let's Do This!")


class TurtleException(Exception):
    """Use this exception to halt command processing if a different error is found.
    Only use if the original error is gracefully handled and you need to stop
    the rest of the command from processing. E.g. a file is not found or args
    are invalid."""
    def __init__(self, error, msg):
        self.error = error
        self.message = msg
        #super.__init__(error)

    def __str__(self):
        return self.error


@bot.event
async def on_message(message):
    global cur_user

    if message.content.startswith(prefix):
        print("Command!")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')

    elif message.author == cur_user:
        await conversate(message)

    elif ("hey turtle" in message.content.lower()):
        await sendmsgorig(message,"What?!")
        cur_user = message.author
        print(cur_user)

    elif "thanks turtle" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "No problem Boss!")
        else:
            await sendmsgorig(message, "Your welcome!")

    elif "please" in message.content.lower(): 
        if message.author.id == bertle:
            await sendmsgorig(message, "PRETTY PLEASE!")

    elif message.author == bot.user:
        print("Im talking:")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')
    #else:
    #   print(message.content)


    await bot.process_commands(message)


if __name__ == '__main__':
    global source_path
    source_path = os.path.dirname(os.path.abspath(__file__)) # /a/b/c/d/e

    #logging.basicConfig(level=logging.ERROR)

    try:
        file = open("Token.txt")
    except:
        file = open('/home/pi/Turtle/Token.txt')
    token = file.read()
    file.close()

    #try:
    #    os.makedirs(os.path.join('resources','soundclips','temp'))
    #except:
    #    pass
    #print(token.strip())
    #input()
    bot.run(token.strip())
