import os
import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "سروالي عندي" in message.content:
        await message.channel.send("سروالك عندك هههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههههه")

    await bot.process_commands(message)

@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("لازم تكون داخل روم صوتي أولاً!")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("البوت مو داخل روم صوتي!")

@bot.command(name='play')
async def play(ctx, url):
    try:
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            if ctx.author.voice:
                voice_client = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("ادخل روم صوتي أولاً!")
                return

        async with ctx.typing():
            info = ytdl.extract_info(url, download=False)
            url2 = info['url']
            voice_client.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS))
        await ctx.send(f'جاري تشغيل: {info["title"]}')
    except Exception as e:
        await ctx.send(f"حدث خطأ أثناء التشغيل: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
