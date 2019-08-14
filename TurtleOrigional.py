'''

 Josh Zack's (Bertle's) Turtle bot

 client id :: 588168168082636802
 permissions integer :: 8

 https://discordapp.com/oauth2/authorize?client_id=588168168082636802&scope=bot&permissions=8

 Todo:
 - looping
 - change images in embed from links to attachments
 - add fire weather effect, among other effects
 - When It's done, Take all of the weather based *functions* and offload them

 Other Features:
 - dice roller
 - code spelling out words (alpha, bravo, delta)
 - poi
 - tarot card readings
 - get actual weather readings
 
 '''

'''
 class LoopingSource(AudioSource):
    def __init__(self, source_factory):
        self.factory = source_factory
        self.source = source_factory()

    def read(self):
        ret = self.source.read()
        if not ret:
            self.source = self.source_factory()
            ret = self.source.read()
        return ret

'''

import discord, random
import asyncio

#from help import helpEmbed

#globals
client = discord.Client()
authorId = 275002179763306517 # bertle
cur_user = 0
#currentWeather = '.\\sounds\\rain.wav'
currStatus = discord.Activity(name="turtle sounds. | []help", type=discord.ActivityType.listening)
#source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(currentWeather))
vol = 0.5
currentClient = 0

#functions

def getText(file):
    with open(file, "r") as f:
        lines = f.read()
        return lines.strip()

def updateSource():
    global source
    #global currentWeather
    global cur_user
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(currentWeather))

async def setVol(num,message):
    global vol
    global source
    if num > 100 or num < 0:
        await message.add_reaction("❌")
    else: 
        vol = num * 0.01
        source.volume = vol
        await message.add_reaction("✔")

async def join(message):
    if message.author.voice is not None:
        await message.author.voice.channel.connect()

async def leave(message):
    await message.guild.voice_client.disconnect()

def randomnum(low,high):
    return random.randrange(low,high+1)

async def sendmsg(message,msg):
    await message.channel.send(msg)

async def dice(message):
    addon = '0'
    
    if "+" in message.content.lower():
        addon = message.content.lower()[message.content.lower().index("+"):]
        message.content = message.content[:message.content.lower().index("+")]
    elif "-" in message.content.lower():
        addon = message.content.lower()[message.content.lower().index("-"):]
        message.content = message.content[:message.content.lower().index("-")]
    
    if "[]r 2d20" in message.content.lower():
        await sendmsg(message,'d20: %i' % (randomnum(1,20)))
        msg = 'd20: %i' % (randomnum(1,20))

    elif (message.content.lower() != "[]r +") and (message.content.lower() != "[]r -") and (message.content.lower() != "[]r"):
        numbers = (message.content.lower().replace("[]r ",''))
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
        await sendmsg(message, msg)
    except:
        await sendmsg(message, "Discord doesent like long stuffs so here is the summup.")
        await sendmsg(message, 'Total: %i' % (randomnum(int(numbers[:split]),int(numbers[split+1:])*int(numbers[:split]))))



async def botsummon(message):
    msg = message.content
    await sendmsg(message, msg)


'''
async def setWeather(weatherIn,message):
    global currentWeather
    global source

    if weatherIn == 'clear':
        currentWeather = 'clear'
        await leave(message)
    else:
        try:
            await join(message)
        except:
            pass
        currentWeather = ".\\sounds\\" + weatherIn + ".wav"
        print(currentWeather)
        updateSource()
        if client.voice_clients[currentClient].is_playing():
            client.voice_clients[currentClient].stop()
        client.voice_clients[currentClient].play(source)
        source.volume = vol

async def play(message):
        client.voice_clients[currentClient].play(discord.FFmpegPCMAudio('.\\sounds\\rain.wav'))

async def weather(message):

    if " help" in message.content.lower(): #help command, tells user the working commands
        await message.author.send(embed=helpEmbed)
        await message.add_reaction("✉")

    elif " rain" in message.content.lower(): # set the weather to rain
        await message.add_reaction("🌧")
        await setWeather("rain",message)

    elif " thunderstorm" in message.content.lower(): # set the weather to a thunderstorm
        await message.add_reaction("⛈")
        await setWeather("storm",message)

    elif " thunder" in message.content.lower(): # set the weather to just thunder
        await message.add_reaction("🌩")
        await setWeather("thunderonly",message)

    elif " fire" in message.content.lower():
        await message.add_reaction("🔥")
        await setWeather("bonfire",message)
    
    elif " clear" in message.content.lower(): # clears the weather
        await message.add_reaction("☀")
        await setWeather("clear",message)

    else: # error
        await message.add_reaction("❔")
'''
@client.event
async def on_ready():
    print(f" {client.user}, Lets do this!")
    await client.change_presence(activity=currStatus)

@client.event 
async def on_message(message): # Basically my Main
    global cur_user
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if message.author == client.user:
        return

    if "[]join" in message.content.lower():
        await join(message)

    if "[]leave" in message.content.lower():
        await leave(message)

    #this is mostly to get info about something
    '''
    if "[]me" in message.content.lower(): # simple ping
        #await sendmsg(message, message.author)
        for a in client.users:
            for b in message.guild.members:
                if b == a:
                    msg = "<@%s>" % (a.id)
                    await sendmsg(message, msg)
    #'''
    if "[]call" in message.content.lower(): # simple ping
        #await sendmsg(message, message.author)
        #person = client.get_user(message.content.lower()[6:])
        #await sendmsg(message,person)
            #msg = "<@%s>" % (a.id)
        await message.author.send("hi")
    
    if message.content.startswith('[]turtle'):
        await message.add_reaction("🐢")


    if "[]help" in message.content.lower(): # simple ping
        await message.author.send("```Functions: \n Hey Turtle: has its own stuff \n []r: roles dice \n []help: Does this. Obviously```")
        #person = client.get_user(message.content.lower()[6:])
        #await sendmsg(message,person)
            #msg = "<@%s>" % (a.id)
        #await client.send_message("Bertle#9579", "hi")
    if "[]bots" in message.content.lower():
        await sendmsg(message,"!get")

    if "[]bottags" in message.content.lower():
        
        failsafe = False
        for role in message.guild.roles:
            if role.name == 'Turtle':
                await message.author.add_roles(role)
                failsafe = True
                break
            else:
                failsafe = False
        if not failsafe:
            await message.guild.create_role(name="Turtle", colour=discord.Colour(0x00ff1f))
            for role in message.guild.roles:
                if role.name == 'Turtle':
                    await message.author.add_roles(role)

    if message.content.startswith('[]r'):
        await dice(message)

    if "hey turtle" in message.content.lower(): # simple ping
        await sendmsg(message, "What?!")
        cur_user = message.author.id
        print(cur_user)
    
    elif cur_user == message.author.id:
        if "make me a sandwich" in message.content.lower(): # simple ping
            await sendmsg(message, "Here you go!")
            await message.channel.send(file=discord.File('Sandwich.jpg'))

        elif "bubble" in message.content.lower(): # simple ping
            await sendmsg(message, "BUBBLES!")

        elif "random" == message.content.lower():
            await sendmsg(message, "RANDOM NUMBERS YOU SAY!?")
            for a in range(randomnum(2,24)):
                await sendmsg(message,randomnum(10,10000))
            await sendmsg(message, "Fin.")

        elif "what time is it" in message.content.lower():
            await sendmsg(message, "TURTLE TIME!")
            msg = "🐢"
            for a in range(randomnum(2,24)):
                msg = msg + "🐢"
            await sendmsg(message, msg)

        elif "i need an army" in message.content.lower():
            await sendmsg(message, "On it boss!")
            msg = "🐢"
            for a in range(randomnum(100,200)):
                msg = msg + "🐢"
            await sendmsg(message, msg)

        elif "yell at " in message.content.lower():
            msg = ("They arnt here, sorry %s." % (message.author.name))
            for users in client.users:
                for b in message.guild.members:
                    if b == users:
                        if message.content.lower()[8:] in users.name.lower():
                            msg = "Hey <@%s>! %s wants you." % (users.id,message.author.name)
            await sendmsg(message, msg)

        elif "help" in message.content.lower():
            await sendmsg(message, "I can yell at someone, make a sandwich, I like bubbles, and randomness...")
            await sendmsg(message, "Helpful?")
        elif "hi" in message.content.lower(): # simple ping
            await sendmsg(message, "Hello!")
        else:# simple ping
            await sendmsg(message, "Ok then!")
        
        cur_user = 0

    elif message.content.lower().startswith('attack'): 
        await sendmsg(message, "Advance! *Turtles march slowly.")

    
    elif "bye turtle" in message.content.lower(): 
        if message.author.id == authorId:
            await sendmsg(message, "Bye!")
            #await message.add_reaction("👋")
            await client.close()
    
    elif "thanks turtle" in message.content.lower(): 
        if message.author.id == authorId:
            await sendmsg(message, "No problem.")


    '''
    if "!say" in message.content.lower():
        await play(message)

    if "!volume" in message.content.lower():
        msg = int(message.content.strip("!volume").strip())
        await setVol(msg,message)
    
    elif "!weather" in message.content.lower(): # weather commands (plays into an internal function for simplicity)
        await weather(message)
    
    elif "!toggledownfall" in message.content.lower(): #toggles between 'clear' and 'rain'
        if currentWeather == 'clear':
            await setWeather('rain',message)
            await message.add_reaction("🌧")
        else:
            await setWeather('clear',message)
            await message.add_reaction("☀")
    '''
    #await await sendmsg(file=discord.File('.\\images\\thenperish.jpg'))


client.run(getText("Token.txt"))