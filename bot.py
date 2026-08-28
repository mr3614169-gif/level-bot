import discord
from discord.ext import commands
import json, os, random
from flask import Flask
import threading

app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"
def run_web():
    app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run_web).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

if os.path.exists("levels.json"):
    with open("levels.json", "r") as f:
        levels = json.load(f)
else:
    levels = {}

@bot.event
async def on_ready():
    print(f"✅ {bot.user} شغال!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = {"xp":0,"level":0}
    levels[user_id]["xp"] += random.randint(10,20)
    xp = levels[user_id]["xp"]
    new_level = int((xp/100)**0.5)
    if new_level > levels[user_id]["level"]:
        levels[user_id]["level"]=new_level
        await message.channel.send(f"🎉 {message.author.mention} طلع لفل **{new_level}**!")
    with open("levels.json","w") as f:
        json.dump(levels,f)
    await bot.process_commands(message)

@bot.command()
async def rank(ctx):
    uid=str(ctx.author.id)
    if uid in levels:
        await ctx.send(f"{ctx.author.name} - لفل {levels[uid]['level']} | XP {levels[uid]['xp']}")
    else:
        await ctx.send("لسه ما بلشت!")

@bot.command()
async def leaderboard(ctx):
    if not levels:
        await ctx.send("ما في حدا لسه!")
        return
    sorted_levels = sorted(levels.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
    msg = "**🏆 التوب 10:**\n"
    for i, (uid, data) in enumerate(sorted_levels, 1):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.name
        except:
            name = f"User {uid}"
        msg += f"{i}. {name} - لفل {data['level']} ({data['xp']} XP)\n"
    await ctx.send(msg)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
