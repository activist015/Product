from supabase import create_client
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Supabase credentials
SUPABASE_URL = "https://fbejbnwsmesbrtsetfir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZiZWpibndzbWVzYnJ0c2V0ZmlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NTgxMzgsImV4cCI6MjA3OTMzNDEzOH0.qMjyM0H-1YYTi1e0PdYeIYPw6Lv5fC-BppdzgUhc3Gk"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Telegram bot token
BOT_TOKEN = "8193801847:AAE1_11kZXBTGpFbE-OMU17zAXGxR12qqXE"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! You will receive top product alerts.")

# Fetch top products
def get_top_products(limit=5):
    response = supabase.table("products").select("*").execute()
    products = response.data
    products.sort(key=lambda x: (x['profit'] or 0, x['demand_score'] or 0), reverse=True)
    return products[:limit]

# Send top products
async def send_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_top_products()
    buttons = [[InlineKeyboardButton(f"{p['product_name']} - Profit: ${p['profit']}", url=p['local_link'])] for p in products]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Top products today:", reply_markup=reply_markup)

# Run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", send_products))
app.run_polling()