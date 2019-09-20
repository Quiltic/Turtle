"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Text to speach Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def text_to_wav(text, ctx, label, speed=0):
    soundclip = generate_id_path(label, ctx)
    file = os.path.join(source_path, soundclip)
    subprocess.call([tts_path, '-r', str(speed), '-o', file, text])
    return soundclip


@bot.command()
async def speakfile(ctx, *args):
    if not args:
        raise discord.InvalidArgument
    to_speak = ' '.join(args)
    await ctx.send(file=discord.File(text_to_wav(to_speak, ctx, 'speakfile', speed=0)))


@bot.command()
async def adderall(ctx, *args):
    if not args:
        raise discord.InvalidArgument
    to_speak = ' '.join(args)
    vc = await connect_to_user(ctx)
    play_text(vc, to_speak, ctx, 'adderall', _speed=7)


@bot.command()
async def speak(ctx, *args):
    if not args:
        raise discord.InvalidArgument
    to_speak = ' '.join(args)
    vc = await connect_to_user(ctx)
    play_text(vc, to_speak, ctx, 'speak')


@bot.command()
async def speakdrunk(ctx, *args):
    if not args:
        raise discord.InvalidArgument
    to_speak = ''.join(args)
    vc = await connect_to_user(ctx)
    play_text(vc, to_speak, ctx, 'speakdrunk', _speed=-10)




"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### Sound Commands ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#loops audio
class LoopingSource(discord.AudioSource):
    def __init__(self, param, source_factory, guild_id):
        self.factory = source_factory
        self.param = param
        self.source = source_factory(self.param)
        self.source.volume = guilds[guild_id].volume
        self.guild_id = guild_id

    def read(self):
        self.source.volume = guilds[self.guild_id].volume
        ret = self.source.read()
        if not ret:
            self.source.cleanup()
            self.source = self.factory(self.param)
            self.source.volume = guilds[self.guild_id].volume
            ret = self.source.read()
        return ret


def play_sound_file(sound, vc, output=True):
    source = source_factory(sound)
    source.volume = guilds[vc.channel.guild.id].volume
    stop_audio(vc)
    vc.play(source)

    if output:
        c = t.CYAN
        print(f'Playing {sound} | at volume: {source.volume} | in: {c}{vc.guild} #{vc.channel}')


def play_text(vc, to_speak, ctx, label, _speed=0):
    sound_file = text_to_wav(to_speak, ctx, label, speed=_speed)
    play_sound_file(sound_file, vc)



def get_guild_sound_path(guild):
    ginfo = guilds[guild.id]
    return ginfo.sound_folder


@bot.command()
async def stop(ctx):
    """Stops any currently playing audio."""
    vc = ctx.voice_client
    stop_audio(vc)

@bot.command()
async def volume(ctx, vol: int):
    fvol = vol / 100
    ginfo = guilds[ctx.guild.id]
    old_vol = ginfo.volume
    ginfo.volume = fvol
    if ctx.voice_client and ctx.voice_client.source: # short-circuit statement
        ctx.voice_client.source.volume = fvol

    react = ctx.message.add_reaction
    speakers = ['🔈','🔉','🔊']
    await react('🔇' if vol is 0 else speakers[min(int(fvol * len(speakers)), 2)])
    await react('⬆' if fvol > old_vol else '⬇')


"""""""""
@bot.command()
async def jermalofi(ctx):
    print('jermalofi')
    vc = await connect_to_user(ctx)
    id = ctx.guild.id
    vc.play(LoopingSource(os.path.join('resources', 'soundclips', 'birthdayloop.wav'), source_factory, id))
#"""""""""

"""""""""
@bot.command()
async def play(ctx, *args):
    if not args:
        raise JermaException('No sound specified in play command.',
                             'Gamer, you gotta tell me which sound to play.')

    sound = ' '.join(args)
    current_sound = get_sound(sound, ctx.guild)
    if not current_sound:
        raise JermaException('Sound ' + sound + ' not found.',
                             'Hey gamer, that sound doesn\'t exist.')

    vc = await connect_to_user(ctx)
    play_sound_file(current_sound, vc)

#"""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
###################### I dont know but I dont want to have this in the main file ###################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def source_factory(filename):
    op = '-guess_layout_max 0'
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename, before_options=op))



def stop_audio(vc):
    if vc.is_playing():
        vc.stop()
        silence = os.path.join('resources', 'soundclips', 'silence.wav')
        play_sound_file(silence, vc, output=False)
        #time.sleep(.07)
        while vc.is_playing():
            continue

"""
def is_major(member):
    if type(member) is commands.Context:
        member = member.author
    for role in member.roles:
        if role.id == 374095810868019200:
            return True
    return False
"""

@bot.command()
async def turtlehelp(ctx):
    avatar = discord.File(os.path.join('resources', 'images', 'avatar.png'), filename='avatar.png')
    thumbnail = discord.File(os.path.join('resources', 'images', 'avatar.png'), filename='thumbnail.png')
    await ctx.author.send(files=[avatar, thumbnail], embed=helpEmbed)
    await ctx.message.add_reaction("✉")



async def help_loop(ctx, msg):
    def check(reaction, user):
        return str(reaction.emoji) in ['⬅', '➡']
    while True: # seconds
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=30,
                                             message=msg, check=check)
        except asyncio.TimeoutError:
            return
        else:
            if str(reaction.emoji) is '⬅':
                msg.edit(embed=helpEmbed)
                msg.remove_reaction(reaction.emoji, reaction.author)
            if str(reaction.emoji) is '➡':
                msg.edit(embed=get_list_embed(guilds[ctx.guild.id]))
                meg.remove_reaction(reaction.emoji, reaction.author)

