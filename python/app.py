import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import asyncio
from pytube import YouTube
from youtubesearchpython import VideosSearch

print("Program Starting")

load_dotenv()
token = os.getenv("TOKEN")

queue = list()

intents = discord.Intents(messages = True, guilds = True, voice_states = True, typing = True)

client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='rick ',intents=intents)

print("Bot Made")

@bot.command(name = 'join', help="To make the bot join the channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name = 'ping', help="Making sure bot is online")
async def ping(ctx):
    await ctx.send("I am here, be not afraid")
    return

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play', help='To play song')
async def play(ctx, *args):
    name = ' '.join(args)

    if name == '':
        name = "Never Gonna Give You Up"

    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        (filename, title) = download_song(name)
        queue.append((title, filename, True))
        async with ctx.typing():
            while True:
                next_song = queue.pop()
                if(not next_song[2]):
                    break
                voice_channel.play(discord.FFmpegPCMAudio(next_song[1]))
                await ctx.send('**Now playing:** {}'.format(title))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

# @bot.command(name='queue', help='Displays the current queue')
# async def queue(ctx):
#     str = ""
#     for song in queue:


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

def download_song(name):
    result = VideosSearch(name, limit = 1).result()
    id = result['result'][0]['id']
    title = result['result'][0]['title']
    link = "https://www.youtube.com/watch?v=" + str(id)

    yt = YouTube(link)
    yt.streams.get_audio_only().download('song_files')
    return ("song_files/" + title + ".mp4", title)

if __name__ == "__main__":
    bot.run(token)