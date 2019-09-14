if __name__ == "__main__":
    import os, subprocess
    import discord
    from discord.ext import commands
    prefix = '[]'
    bot = commands.Bot(prefix)
    import pigpio, asyncio
    pi = pigpio.pi()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Light Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from datetime import datetime
Lights = {"Color": [255,255,255], "On?": False, "Delay": 60}


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
"""
async def connect_lights(ctx ,red = 0, green = 0, blue = 0):
    '''Eventualy will do all the lights stuff witht the IO of the pi'''
    print("colors")
    
    
    #Turn on the lightpins (will work even if this fails)
    #os.system("sudo pigpiod")
    #Red
    cmd = ["pigs", "p" ,"17", str(red)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    #for out in output:
    await ctx.send("Redchange")
    await asyncio.sleep(.1)
        
    #green
    cmd = ["pigs", "p" ,"22", str(green)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    await ctx.send("Greenchange")
    await asyncio.sleep(.1)
    #for out in output:
    #    await ctx.send(out)
        
    #blue
    cmd = ["pigs", "p" ,"24", str(blue)]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE ).communicate()
    await ctx.send("Bluechange")
    #for out in output:
    #    await ctx.send(out)
#"""
'''

#@bot.command()
async def light(ctx, color = None):
    """This is the Utility to change the lights in my room. Light Wizards ONLY!"""
    colors = {"blue": [0,0,255], "red": [255,0,0], "green": [0,255,0], "white": [255,255,255]}
    global Lights
    if await light_perms(ctx):
        if color == None:
            Lights["On?"] = (not Lights["On?"])
            if Lights["On?"]:
                await ctx.send("Lights on! *Clap* *Clap*")
                await light_wampin()
            else:
                await ctx.send("Lights off! *Clap* *Clap*")
        else:
            if (not Lights["On?"]):
                Lights["On?"] = True
                await ctx.send("Lights on! *Clap* *Clap*")
                await light_wampin()
            
            try:
                Lights["Color"] = colors[color]
                msg = "Color set to %s." % (color)
                await ctx.send(msg)
            except:
                await ctx.send("That color isent in the registry! Do '[]newcolor name red green blue' to set it!")



#@bot.command()
async def newcolor(ctx, name, red, green, blue):
    """Adds a new color to the registry."""
    colors = {} #get the current colors from a file called colors its a dictionary
    colors[(name.lower())] = [int(red), int(green), int(blue)]
    #Save the colors to the file then move on


    msg = "New color has been saved as %s." % (name)
    await ctx.send(msg)



async def light_wampin():
    """
    This is the startup for the lights it only runs when Lights["On?"] == True
    
    It is to be used to change the brightness of the lights based on the time of day and the weather
    """
    await bot.get_user(bertle).send("Lights on!")
    now = datetime.now()
 
    print("now =", now)
    # dd/mm/YY H:M:S
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print("time =", dt_string)
    #while (int(dt_string[6:]) > 5):
    while (Lights["On?"] == True):
        #This is to get it to run for every diration and in turtle to get the time/weather for brightness 
        #print(int(dt_string[6:]),60-int(dt_string[6:]))
        #await asyncio.sleep(60-int(dt_string[6:]))
        await asyncio.sleep(Lights["Delay"])
        #now = datetime.now()
        #dt_string = now.strftime("%H:%M:%S")


    await bot.get_user(bertle).send("Lights off!")



'''





    

