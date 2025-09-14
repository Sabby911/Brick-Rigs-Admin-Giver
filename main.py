import os
import time
import win32gui
from dotenv import load_dotenv
import discord
from discord.ext import commands
from function import grant_admin  # Import your admin function

# Load .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Only allow these users to run !admin
AUTHORIZED_USERS = ["YourDiscordUsername#1234"]

# Track Brick Rigs window
BRwindowopen = False
BRwindowclose = True
last_state = None

def is_brickrigs_open():
    """Check if a window titled 'Brick Rigs' exists"""
    def callback(hwnd, windows):
        if "Brick Rigs" in win32gui.GetWindowText(hwnd):
            windows.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return len(windows) > 0

async def monitor_window():
    """Background task to monitor Brick Rigs window and send Discord updates"""
    global BRwindowopen, BRwindowclose, last_state
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found. Check CHANNEL_ID.")
        return

    while not bot.is_closed():
        BRwindowopen = is_brickrigs_open()
        BRwindowclose = not BRwindowopen

        if BRwindowopen and last_state != "open":
            last_state = "open"
            print("Brick Rigs window is OPEN")
            await channel.send("🟢 Brick Rigs window is now OPEN!")
        elif BRwindowclose and last_state != "close":
            last_state = "close"
            print("Brick Rigs window is CLOSED")
            await channel.send("🔴 Brick Rigs window is now CLOSED!")

        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=3))

@bot.command()
async def admin(ctx, target: str):
    """Grant admin in Brick Rigs via admin.ini"""
    author = str(ctx.author)
    if author not in AUTHORIZED_USERS:
        await ctx.send("❌ You are not authorized to use this command.")
        return

    if not BRwindowopen:
        await ctx.send("❌ Cannot grant admin: Brick Rigs is not running.")
        return

    success = grant_admin(target)  # Call the function

    if success:
        await ctx.send(f"✅ Admin granted to {target} in Brick Rigs.")
    else:
        await ctx.send(f"❌ Failed to grant admin to {target}.")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    bot.loop.create_task(monitor_window())

bot.run(TOKEN)
