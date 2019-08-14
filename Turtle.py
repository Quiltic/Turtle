import asyncio, discord, subprocess
import time, random, os, sys
from discord.ext import commands
#from pydub import AudioSegment
#from guild_info import GuildInfo

#from help import helpEmbed, get_list_embed, make_sounds_dict, get_rand_activity

#tts_path = 'resources/voice.exe'

prefix = '[]'
bot = commands.Bot(prefix)
currStatus = discord.Activity(name="turtle sounds. | []help", type=discord.ActivityType.listening)

#get home directory
cwd = os.getcwd()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Custom Admin Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@bot.command()
async def update(ctx):
    print("On")
    #go home you lazy bumb
    os.system(("cd "+ cwd))

    print("changed cd")
    #open update
    callfreind = "python " + cwd + "/TurtleUpdate.py"
    print(callfreind)
    subprocess.Popen(callfreind)
    print("Summoned!")
    
    #turn off
    perish(ctx)

    
def rename_file(old_filepath, new_filepath):
    os.rename(old_filepath, new_filepath)


def getText(file):
    with open(file, "r") as f:
        lines = f.read()
        return lines.strip()


def check_perms(user, action):
    if action is 'update':
        if get_bertle() == user:
            return
        else:
            raise TurtleException('invalid permissions to update',
                                 'You don\'t got permission to do that, pardner.')
    else:
        raise NotImplementedError()


def get_bertle():
    return bot.get_user(bot.owner_id)



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
async def r(ctx, *args):
    stuff = await dice(ctx, *args)
    await sendmsg(ctx,stuff)


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

@bot.command()
async def Yell(ctx):
    await sendmsg(ctx,"AGGGG")

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Basic Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#this is broken?
async def sendmsg(ctx,msg):
    await ctx.send(msg)

def randomnum(low,high):
    return random.randrange(low,high+1)


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
    _ = await connect_to_user(ctx)

#leave the voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        loc = os.path.join('resources', 'soundclips', 'leave')
        #sounds = make_sounds_dict(loc)
        #soundname = random.choice(list(sounds.values()))
        #sound = os.path.join(loc, soundname)
        #play_sound_file(sound, ctx.voice_client)
        time.sleep(1)
        await ctx.guild.voice_client.disconnect()



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
######################  This and Main Stuff was taken from Ben Rucker ######################
                         https://github.com/benrucker
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Turn off
@bot.command()
async def perish(ctx):
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

    if message.content.startswith(prefix):
        print("Command!")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')
    elif message.author == bot.user:
        print("Something else.")
        print(f'{message.author.name} - {message.guild} #{message.channel}: {message.content}')

    await bot.process_commands(message)


if __name__ == '__main__':
    global source_path
    source_path = os.path.dirname(os.path.abspath(__file__)) # /a/b/c/d/e

    #logging.basicConfig(level=logging.ERROR)

    file = open('Token.txt')
    token = file.read()
    file.close()

    #try:
    #    os.makedirs(os.path.join('resources','soundclips','temp'))
    #except:
    #    pass

    bot.run(token.strip())
