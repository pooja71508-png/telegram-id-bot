from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import random, string, os

BOT_TOKEN = "8824123542:AAH8x1PPoE6e_pSJdkmy5e3yrl44gQFFGKU"
ADMIN_CHAT_ID = 7038610091

NAME, MOBILE = range(2)

def gen_userid():
    return "TG" + str(random.randint(10000,99999))

def gen_pass():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome\n\nApna Name bhejiye:")
    return NAME

async def get_name(update: Update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Mobile Number bhejiye:")
    return MOBILE

async def get_mobile(update: Update, context):
    uid = gen_userid()
    pwd = gen_pass()

    name = context.user_data["name"]
    mobile = update.message.text

    await update.message.reply_text(
f"""✅ ID Created

User ID: {uid}
Password: {pwd}
""")

    await context.bot.send_message(
        ADMIN_CHAT_ID,
f"""NEW USER

Name: {name}
Mobile: {mobile}

User ID: {uid}
Password: {pwd}
"""
    )

    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Cancelled")
    return ConversationHandler.END

app = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        MOBILE:[MessageHandler(filters.TEXT & ~filters.COMMAND, get_mobile)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

app.add_handler(conv)
print("Bot Running...")
app.run_polling()
