import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# 🌐 Start Flask server เพื่อกัน Replit หลับ (ใช้ได้ทั้ง Replit / Render)
keep_alive()

# 🔐 โหลดค่าจาก .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))

# 🧠 ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# 👑 Bot Class พร้อม Slash Command
class LucBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)


    async def setup_hook(self):
        # 👇 Sync Command ให้กับ Server ที่กำหนดไว้ (แสดงผลทันที)
        guild = discord.Object(id=GUILD_ID)
        await self.tree.sync(guild=guild)
        print("✅ Slash Commands synced ให้เซิร์ฟเวอร์เรียบร้อยแล้ว!")

bot = LucBot()

# 💬 Slash Command: /status
@bot.tree.command(name="status", description="ตรวจสอบสถานะของบอท")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("✅ บอทยังทำงานอยู่เจ้าค่ะ!")

# ⚡ เมื่อบอทออนไลน์
@bot.event
async def on_ready():
    print(f"บอทพร้อมใช้งานในชื่อ {bot.user}")

# 🔔 ตรวจจับข้อความจาก Announcement Channel
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

# 🚀 เริ่มทำงาน
bot.run(TOKEN)
