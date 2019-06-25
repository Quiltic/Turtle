'''

 Josh Zack's (Bertle's) Turtle bot

 client id :: 588168168082636802
 permissions integer :: 8

 https://discordapp.com/oauth2/authorize?client_id=588168168082636802&scope=bot&permissions=8

 Todo:
 - loot boxs
 - army game
 - fix echo

 Other Features:
 - dice roller
 - code spelling out words (alpha, bravo, delta)
 
 
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

import discord, random, time, os
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
            
            if addon != '0':
                total = int(eval(str(total)+addon))
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
    os.system("Babyturtle.py")
    time.sleep(20)
    await sendmsg(message, "!drip")

class StreamSink(discord.AudioSink):


    def __init__(self, _sink, ctx, user, vc):
        #super().__init__(destination, self._predicate)
        #self.keyword_listener = LocalDecoder()
        #self.keyword_listener.start_streams(stream=self)
        self.ctx = ctx
        self.sink = bytearray()
        #self.stream = stream
        self.user = user
        self.vc = vc
        self.stop = False
        self.other_sink = _sink
        self.delay = 100
        self.past = []
        self.distintpast = 0
        self.looped = False
        #bot.dispatch('start_listen', ctx, self.keyword_listener)


    def write(self, data):
        #if not self.stop:
        if data.user == self.user and not self.stop:
            #self.vc.send_audio_packet(data.data)
            #print(type(data.data))
            #for (x,y) in enumerate(data.data):
            #    print (x, y)
            #new_data = bytes([y for (x,y) in enumerate(data.data) if x % 3 == 0])
            #self.sink.extend(new_data)
            #_sink.write(data)
            #print(len(data.data))
            #self.stream.write(data.data)

            if self.distintpast >= self.delay:
                self.looped = True
                self.distintpast = 0
            else:
                self.distintpast += 1

            if self.looped:
                try:
                    self.vc.send_audio_packet(self.past[self.distintpast-1].data)
                    self.past[self.distintpast-1] = (data)
                    
                except:
                    print(self.distintpast, len(self.past))
                    
            else:
                self.past.append(data)
                
            
            #self.vc.send_audio_packet(data.data)

            
            
            #self.vc.send_audio_packet(self.testmorph(data.data))
            #stop = self.keyword_listener.listen_for_keyword(data.data)

    def testmorph(self, data):
        #return bytes([data[x * 2 % len(data)] for x in range(len(data))])
        return bytes([data[x] for x in range(len(data))])

    def read(self, size=1024):
        """Return data array of size size if enough data has been written."""
        if len(self.sink) < 1024:
            return None
        out = self.sink[:size]
        self.sink = self.sink[size:]
        #print(len(out))
        return bytes(out)



async def passthrough(message):
    vc = await message.author.voice.channel.connect()
    user = message.author

    CHUNK = 1024

    #wf = wave.open('test.wav', 'rb')

    sink = discord.AudioSink()
    user_sink = discord.UserFilter(sink, user)
    # sink = StreamSink(user_sink, ctx)

    # p = pyaudio.PyAudio()
    # #
    # stream = p.open(format=p.get_format_from_width(Decoder.SAMPLE_SIZE//Decoder.CHANNELS),
    #                 channels=Decoder.CHANNELS,
    #                 #channels=1,
    #                 #rate=Decoder.SAMPLING_RATE,
    #                 rate=16000,
    #                 output=True)

    # print('format =', p.get_format_from_width(Decoder.SAMPLE_SIZE//Decoder.CHANNELS))
    # print('channels =', Decoder.CHANNELS)
    # print('rate =', Decoder.SAMPLING_RATE)

    sink = StreamSink(user_sink, message, user, vc)

    vc.listen(sink)
    #vc.play(discord.PCMAudio(stream))




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
        vc = await message.author.voice.channel.connect()
        
    if "[]eco" in message.content.lower():
        await passthrough(message)

    if "[]summon" in message.content.lower():
        await botsummon(message)

    if "[]leave" in message.content.lower():
        await leave(message)

    if "[]count" in message.content.lower():
        id = message.id
        #for a in client.get_all_channels():
        #    if message.channel in a:
        #        print(a)
                
        await message.add_reaction("🐢")
        time.sleep(5)
        mess = await message.channel.fetch_message(id)
        print(mess.reactions.count("🐢"))

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

    if "[]pester" in message.content.lower(): # simple ping
        
        msg = ("Can't see them, sorry %s." % (message.author.name))
        for users in client.users:
            if message.content.lower()[9:] in users.name.lower():
                msg = "Hey <@%s>! %s wants you." % (users.id,message.author.name)
                user = users

        if "Can" not in msg:
            for a in range(100):  
                await user.send(msg)
                time.sleep(5)
        else:
            await sendmsg(message, msg)
    
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

    if "[]end" in message.content.lower():
        await client.close()

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
        
        elif "how do i make" in message.content.lower():
            if "banana snaps" in message.content.lower():
                await sendmsg(message, "First you get a banana.")
                time.sleep(1)
                await sendmsg(message, "Then you get a pan.")
                time.sleep(1)
                await sendmsg(message, "Then you find Gabe...")
                time.sleep(1)
                await sendmsg(message, "and you make him do it.")
            elif "sole stone" in message.content.lower():
                await sendmsg(message, "You find one rock.")
                time.sleep(1)
                await sendmsg(message, "Thats it.")
            elif "soul stone" in message.content.lower():
                await sendmsg(message, "You find one rock.")
                time.sleep(1)
                await sendmsg(message, "You then take your soul...")
                time.sleep(1)
                await sendmsg(message, "and put it in...")
                time.sleep(1)
                await sendmsg(message, "the soul compressor.")
                time.sleep(1)
                await sendmsg(message, "Make sure to not drop the rock who knows where it will go.")
                time.sleep(1)
                await sendmsg(message, "Eventualy your soul will find the rock.")
                time.sleep(1)
                await sendmsg(message, "And you have a soul stone.")
            else:
                await sendmsg(message, "No idea, sorry.")

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