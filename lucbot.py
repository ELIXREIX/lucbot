import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

keep_alive()
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(bot)  # 👈 สำหรับ Slash Command

@bot.event
async def on_ready():
    await tree.sync()
    print(f"บอทพร้อมใช้งานในชื่อ {bot.user}")

@bot.tree.command(name="status", description="ตรวจสอบสถานะของบอท")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("✅ บอทยังทำงานอยู่เจ้าค่ะ!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == ANNOUNCE_CHANNEL_ID:
        user = await bot.fetch_user(OWNER_ID)
        await user.send(
            f"📢 แจ้งเตือนจากประกาศ:\n\n{message.content or '[ไม่มีข้อความ text แต่มี embed หรือลิงก์]'}"
        )

    await bot.process_commands(message)

bot.run(TOKEN)
