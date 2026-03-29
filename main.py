import discord
from discord.ext import commands, tasks
import random
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# 📅 DESAFIOS (MELHORADOS)
# ==============================

desafios = [
    "♟️ Xadrez: Mate em 2",
    "🎮 Minecraft: sobreviva 1 noite sem dano",
    "🔫 Valorant: faça 5 kills em uma partida",
    "🎯 Overwatch: jogue 1 partida sem morrer",
    "💣 CS: ganhe uma partida com mais de 10 kills"
]

# ==============================
# 😂 MEMES MELHORES (REDDIT API)
# ==============================

def pegar_meme():
    subreddits = ["memes", "dankmemes", "shitposting"]
    subreddit = random.choice(subreddits)
    url = f"https://meme-api.com/gimme/{subreddit}"
    response = requests.get(url).json()
    return response["url"]

# ==============================
# 🔁 LOOP DIÁRIO
# ==============================

@tasks.loop(hours=24)
async def rotina_diaria():
    canal = bot.get_channel(1454921915130052689)

    if canal:
        desafio = random.choice(desafios)
        meme = pegar_meme()

        await canal.send(f"🔥 **DESAFIO DO DIA**\n{desafio}")
        await canal.send(f"💀 **MEME DO DIA**\n{meme}")

# ==============================
# 🔁 LOOP SEMANAL
# ==============================

@tasks.loop(hours=168)
async def rotina_semanal():
    canal = bot.get_channel(1454921915130052689)

    if canal:
        await canal.send("🏆 **DESAFIO SEMANAL**\nVença 3 desafios da semana!")

# ==============================
# 📩 COMANDOS
# ==============================

@bot.command()
async def meme(ctx):
    await ctx.send(pegar_meme())

@bot.command()
async def desafio(ctx):
    await ctx.send(random.choice(desafios))

# ==============================
# 🎰 SISTEMA DE CASSINO (BASE)
# ==============================

saldo = {}

@bot.command()
async def daily(ctx):
    user = ctx.author.id
    saldo[user] = saldo.get(user, 0) + 100
    await ctx.send(f"💰 {ctx.author.mention}, você ganhou 100 moedas!")

@bot.command()
async def saldo_cmd(ctx):
    user = ctx.author.id
    await ctx.send(f"💳 Saldo: {saldo.get(user, 0)} moedas")

@bot.command()
async def apostar(ctx, valor: int):
    user = ctx.author.id

    if saldo.get(user, 0) < valor:
        await ctx.send("❌ Saldo insuficiente!")
        return

    if random.random() < 0.5:
        saldo[user] += valor
        await ctx.send("🎉 Você ganhou!")
    else:
        saldo[user] -= valor
        await ctx.send("💀 Você perdeu!")

# ==============================
# ♟️ XADREZ (BASE SIMPLES)
# ==============================

@bot.command()
async def chess(ctx):
    moves = ["e4", "d4", "Nf3", "c4"]
    move = random.choice(moves)
    await ctx.send(f"♟️ Jogada do bot: {move}")

# ==============================
# 🚀 START
# ==============================

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    rotina_diaria.start()
    rotina_semanal.start()

bot.run(TOKEN)