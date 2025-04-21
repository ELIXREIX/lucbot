import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# เปิด Flask server กันบอทหลับ (ใช้กับ Replit ได้)
keep_alive()

# โหลด ENV
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID"))

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# สร้าง Bot Class
class LucBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()  # ✅ ใช้ Global Sync แทน Guild Sync
        print("✅ Global Slash Commands synced เรียบร้อยแล้วเจ้าค่ะ!")

bot = LucBot()

# /status
@bot.tree.command(name="status", description="ตรวจสอบสถานะของบอท")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("✅ บอทยังทำงานอยู่เจ้าค่ะ!")

# /ping
@bot.tree.command(name="ping", description="ดูความเร็วในการตอบของบอท")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! ความหน่วง: `{latency}ms`")

# /info
@bot.tree.command(name="info", description="ข้อมูลของบอท Luc Bot")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 Luc Bot ผู้รับใช้ที่ซื่อสัตย์ของนายท่าน สร้างด้วย Python และหัวใจเมดค่ะ 💕")

# /purge
@bot.tree.command(name="purge", description="ลบข้อความตามจำนวนที่ระบุ (เฉพาะผู้มีสิทธิ์)")
@app_commands.describe(amount="จำนวนข้อความที่ต้องการลบ (สูงสุด 100)")
async def purge(interaction: discord.Interaction, amount: int):
    if not interaction.channel.permissions_for(interaction.user).manage_messages:
        await interaction.response.send_message("❌ คุณไม่มีสิทธิ์ในการลบข้อความนะเจ้าคะ!", ephemeral=True)
        return

    if amount < 1 or amount > 100:
        await interaction.response.send_message("⚠️ ใส่จำนวนระหว่าง 1 ถึง 100 เจ้าค่ะ", ephemeral=True)
        return

    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 ลบข้อความจำนวน {len(deleted)} ข้อความเรียบร้อยแล้วเจ้าค่ะ!", ephemeral=True)

# /summon_maid
@bot.tree.command(name="summon_maid", description="เรียกเมดประจำตัวมารายงานตัวเจ้าค่ะ!")
async def summon(interaction: discord.Interaction):
    embed = discord.Embed(title="เมดดิชั้นรายงานตัว!", description="พร้อมรับใช้เสมอค่ะนายท่าน 💖", color=0xFFC0CB)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1053/1053244.png")
    await interaction.response.send_message(embed=embed)

# เมื่อตัวบอทพร้อม
@bot.event
async def on_ready():
    print(f"บอทพร้อมใช้งานในชื่อ {bot.user}")

# ตรวจจับข้อความประกาศแล้ว DM หานายท่าน
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

# เริ่มรันบอท
bot.run(TOKEN)