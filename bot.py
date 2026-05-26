from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8931408596:AAHpQAeA0iLWLQjrltfJ1RZYfrh5HNrSbGQ"

# OWNER ID
OWNER_ID = 8722144519

# SUDO USERS
SUDO_USERS = {OWNER_ID}

# MUTED USERS
MUTED_USERS = set()


# START MESSAGE
START_TEXT = """
🔥 GETO MUTE BOT 🔥

━━━━━━━━━━━━━━━
⚡ AVAILABLE COMMANDS ⚡
━━━━━━━━━━━━━━━

➤ .mute
Reply to a user to auto delete all messages.

➤ .unmute
Reply to unmute the user.

➤ /add
Reply to give sudo access.

➤ /del
Reply to remove sudo access.

━━━━━━━━━━━━━━━
👑 OWNER & SUDO USERS
MESSAGES NEVER DELETE
━━━━━━━━━━━━━━━

💀 TAKE SUDO FROM:
JAKE GETO
"""


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)


# /add
async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to user with /add"
        )
        return

    user_id = update.message.reply_to_message.from_user.id

    SUDO_USERS.add(user_id)

    await update.message.reply_text(
        "✅ User added as sudo"
    )


# /del
async def del_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to user with /del"
        )
        return

    user_id = update.message.reply_to_message.from_user.id

    if user_id == OWNER_ID:
        await update.message.reply_text(
            "❌ Cannot remove owner"
        )
        return

    SUDO_USERS.discard(user_id)

    await update.message.reply_text(
        "❌ User removed from sudo"
    )


# .mute
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id

    if sender_id not in SUDO_USERS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user with .mute"
        )
        return

    target_id = update.message.reply_to_message.from_user.id

    # protect owner/sudo
    if target_id in SUDO_USERS:
        await update.message.reply_text(
            "❌ Cannot mute sudo/owner"
        )
        return

    MUTED_USERS.add(target_id)

    await update.message.reply_text(
        "🔇 User muted"
    )


# .unmute
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id

    if sender_id not in SUDO_USERS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user with .unmute"
        )
        return

    target_id = update.message.reply_to_message.from_user.id

    MUTED_USERS.discard(target_id)

    await update.message.reply_text(
        "🔊 User unmuted"
    )


# DELETE MUTED USER MESSAGES
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id

        # Never delete sudo/owner messages
        if user_id in SUDO_USERS:
            return

        # Delete muted user messages
        if user_id in MUTED_USERS:
            await update.message.delete()

    except:
        pass


def main():
    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # /add
    app.add_handler(
        CommandHandler("add", add_sudo)
    )

    # /del
    app.add_handler(
        CommandHandler("del", del_sudo)
    )

    # .mute
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^\.mute$"),
            mute_user
        )
    )

    # .unmute
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^\.unmute$"),
            unmute_user
        )
    )

    # DELETE
    app.add_handler(
        MessageHandler(
            filters.ALL,
            delete_messages
        )
    )

    print("🔥 GETO BOT RUNNING 🔥")

    app.run_polling()


if __name__ == "__main__":
    main()
