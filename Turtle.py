#import asyncio, subprocess
#import time, random, os, sys
#from datetime import datetime

#from wether import *
#from Lights import *

from Tools import *

try:
    print("Trying to import discord!")
    os.system("python3 -m pip install --upgrade discord.py")
    import discord
    from discord.ext import commands
except:
    print("Cant import just recollecting it.")
    os.system("python3 -m pip install discord.py")
    import discord
    from discord.ext import commands


"""
Todo:
    Lighting for turthe
    - check for sunrize/set
    -  
    Timmer
    - add until x time, 




"""


#from pydub import AudioSegment
#from guild_info import GuildInfo

#from help import helpEmbed, get_list_embed, make_sounds_dict, get_rand_activity

#tts_path = 'resources/voice.exe'


""" Basic startup for a discord bot"""
prefix = ('[] ', '[]')
bot = commands.Bot(prefix)#, connector=aiohttp.TCPConnector(ssl=False)
curr_status = discord.Activity(name="turtle sounds. | []help", type=discord.ActivityType.listening)

#get home directory
cwd = os.getcwd()

bertle = 275002179763306517 #my id  #bot.get_user(bot.owner_id)
cur_user = 0 # the curent user that is talking to turtle


lights_info = {"Color": [0,0,0], "On?": False, "Delay": 60, "User": 0} #all of the info for the lights




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@bot.command()
async def showTerminal(ctx, *args):
    """ Basicly is an ssh into the rasberry pi """
    cmd = []
    for a in args:
        cmd.append(a)
    print(cmd)

    if await check_perms(ctx):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate() # the part that runs the command into the terminal
        #output = pipe.read()
        for out in output:
            #words = "```" + out + "```"
            await ctx.send(out) # Print the output of the terminal, it will look weard because it keeps the "b " and \n dont know why
    else:
        await ctx.send("Failed!")

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
        call_freind = "python3 /home/pi/Turtle/TurtleUpdate.py &"
        print(call_freind)
        os.system(call_freind)
        #subprocess.Popen(callfreind)

        await sendmsg(ctx,"Opened Friend!")
        print("Summoned!")
        
        #turn off
        await turnoff(ctx)
    else:
        await ctx.send("Failed!")


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
    else:
        await ctx.send("Failed!")


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
    else:
        await ctx.send("Failed!")




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
###################### Light Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.command()
async def light(ctx, brightness = 100):
    """This basicly makes it a set color per person"""

    global lights_info
    brightness = brightness/100 # how bright the lights are
    await ctx.message.add_reaction("💡")

    if await light_perms(ctx):
        #Turns off the lights
        if ((ctx.author.id == lights_info["User"]) and (max(lights_info["Color"]) == 255)):
            await connect_lights(ctx, int(0), int(0), int(0))
            lights_info["User"] = 0
            lights_info["Color"] = [0,0,0]
            await ctx.send("Turned off!")

        #my color
        elif (ctx.author.id == bertle):
            lights_info["User"] = ctx.author.id
            lights_info["Color"] = [int(220*brightness),int(255*brightness),int(190*brightness)]
            await connect_lights(ctx, lights_info["Color"][0], lights_info["Color"][1], lights_info["Color"][2])  # Change the color
            await ctx.send("Changed!")

        #roomates color
        elif (ctx.author.id == 73486425349165056):
            lights_info["User"] = ctx.author.id
            lights_info["Color"] = [int(255*brightness),int(130*brightness),int(10*brightness)]
            await connect_lights(ctx, lights_info["Color"][0], lights_info["Color"][1], lights_info["Color"][2])  # Change the color
            await ctx.send("Changed!")



        else:
            #if someone is a light wizard but doesent have a set color
            await ctx.send(ctx.author.id)
            await ctx.send("Use setcolor instead!")



@bot.command()
async def setcolor(ctx, red = 0, green = 0, blue = 0):
    """Changes the color to be ____."""
    global lights_info 
    print("check")

    if await light_perms(ctx):
        print("started")

        await connect_lights(ctx,red,green,blue) # Change the color
        
        msg = "Color set to %s, %s, %s." % (red,green,blue)
        await ctx.send(msg)
        await ctx.message.add_reaction("💡")

        lights_info["User"] = ctx.author.id
        lights_info["Color"] = [red,green,blue]


@bot.command()
async def brightness(ctx, bright = 100):
    """Changes the brightness of the current color without changing the base color"""
    global lights_info
    if await light_perms(ctx):
        top = 255-max(lights_info["Color"])#makes it into the highest values for the type of light basicly seting its brightness to 100%
        
        bright = bright/100 # sets the brightness to a %

        #suposidly makes the colors into the max val and saves it, suposidly
        lights_info["Color"] = [int((lights_info["Color"][0]+top)*bright), int((lights_info["Color"][1]+top)*bright), int((lights_info["Color"][2]+top)*bright)]
        #for a in lights_info["Color"]:
        #    a += top

        await connect_lights(ctx, int(lights_info["Color"][0]), int(lights_info["Color"][1]), int(lights_info["Color"][2]))    
        #await connect_lights(ctx, int(lights_info["Color"][0]*bright), int(lights_info["Color"][1]*bright), int(lights_info["Color"][2]*bright)) # incase the above doesent work uncomment me
        await ctx.send("Brightness changed.")



@bot.command()
async def color(ctx):
    """ Get the curent RBG for the color displayed """
    await ctx.send("The current color is %s" % lights_info["Color"])



@bot.command()
async def fade(ctx , fade_time = 10, red_out = 255, blue_out = 255, green_out = 255, red_in = None, green_in = 0, blue_in = 0):
    """ Fades between two colors over x time (time reds_end greens_end blues_end begining_red begining_green begining_blue)"""
    
    # So for some reason I cant just put this into the filler, thus it has to be done like this
    if red_in == None:
        red_in = lights_info["Color"][0]
        green_in = lights_info["Color"][1]
        blue_in = lights_info["Color"][2]
    
    if light_perms(ctx):
        await ctx.message.add_reaction("🌈")
        await fadebetween(ctx ,red_in, green_in, blue_in, red_out, blue_out, green_out, fade_time)
        await ctx.send("Faided!")
        


#anoyingly only works in this file due to connect_lights, and cant be moved into another file.
async def fadebetween(ctx ,red_in = 0, green_in = 0, blue_in = 0, red_out = 255, green_out = 255, blue_out = 255, fade_time = 10):
    """ Used to have any function fade not just the one command """
    global lights_info
    fade_time = float(fade_time*10) # makes it so that it changes 10 times a second, mostly for lower time amounts like 1 or 5

    # To incrimentlaly change the colors over a set time evenly
    red_fade = ((red_out-red_in)/(fade_time))
    green_fade = ((green_out-green_in)/(fade_time))
    blue_fade = ((blue_out-blue_in)/(fade_time))
    
    # Achual fading
    for steps in range(int(fade_time)):
        #print((red_in+(red_fade*steps)),(green_in+(green_fade*steps)),(blue_in+(blue_fade*steps)))
        await connect_lights(ctx,int(red_in+(red_fade*steps)),int(green_in+(green_fade*steps)),int(blue_in+(blue_fade*steps)))
        await asyncio.sleep(.01) # so that other commands can be run in the meantime. Yes this command slows turtle, but it is coooooollllll
    
    await connect_lights(ctx, red_out, green_out, blue_out) # it doesent ever make it the final color without this

    
    lights_info["Color"] = [red_out,green_out,blue_out] # change the color of the lights to this
    



#anoyingly only works in this file, and cant be moved into another file.
async def connect_lights(ctx ,red = 0, green = 0, blue = 0):
    """Does all the lights stuff with the IO of the pi"""
    print("colors")  # this dident work with os.system() and so I used subprocess
    #Red
    cmd = ["pigs", "p" ,"17", str(red)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    #await ctx.send("Redchange")
    #await asyncio.sleep(.01)
        
    #green
    cmd = ["pigs", "p" ,"22", str(green)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    #await ctx.send("Greenchange")
    #await asyncio.sleep(.01)
        
    #blue
    cmd = ["pigs", "p" ,"24", str(blue)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    #await ctx.send("Bluechange")



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.command()
async def tofraction(ctx, des):
    """ Given a decimal return a fraction """
    outa, outb = fraction_finder(des)
    await ctx.send("The decimal %s becomes %s/%s." % (des,outa, outb))
    

@bot.command()
async def timmer(ctx, delay = 5, tpe = 'sec', msg = None):
    """ Makes me set a timemer for # then ⏰
        Usage []timmer amount min/sec/hour
        Default is:  5 sec
    """
    if tpe == 'min':
        delay *= 60 
    if tpe == 'hour':
        delay *= 3600

    await ctx.send(("Counting down from: %s" % (delay)))
    await asyncio.sleep(delay)
    await ctx.send("@{} Times up!".format(ctx.author.id))
    await ctx.message.add_reaction("⏰")
    if msg != None:
        await ctx.send(msg)
    


@bot.command()
async def weather(ctx):
    """Tells you the current weather"""
    #sadly only works for cincinati for now

    await ctx.message.add_reaction("🐢")
    data = advanced_weather()

    #shows the achual info
    msg = "Currently: " + data["Description"]
    time_stuff = "Around: "+ data["Time"]
    forcast=discord.Embed(title=time_stuff, description=msg, color=0x1c57e3)
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
    await ctx.message.add_reaction("🎲")
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



# this is from old turtle but i still love it
async def conversate(message):
    global cur_user

    if "make me a sandwich" in message.content.lower(): # simple ping with a file
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
        #pi.stop()
        await bot.close()

#Turn off for the bot to use when updating
async def turnoff(ctx):
    await sendmsg(ctx,"Restarting?")
    print("Bye!")
    #pi.stop()
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
    #global guilds
    await bot.change_presence(activity=curr_status)

    #guilds = dict()
    #for guild in bot.guilds:
    #    guilds[guild.id] = GuildInfo(guild)

    #print(f'Logged into {str(len(guilds))} guilds:')
    #for guild in list(guilds.values()):
    #    print(f'\t{guild.name}:{guild.id}')


    #Turn on the lightpins
    os.system("sudo pigpiod")

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


    elif message.content.startswith("[] "): 
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
