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

# Access users
ACCESS_USERS = {OWNER_ID}

# Muted users
MUTED_USERS = set()


# /add user_id
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])

        ACCESS_USERS.add(user_id)

        await update.message.reply_text(
            f"✅ Added {user_id}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/add user_id"
        )


# /del user_id
async def del_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])

        if user_id == OWNER_ID:
            return

        ACCESS_USERS.discard(user_id)

        await update.message.reply_text(
            f"❌ Removed {user_id}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/del user_id"
        )


# .mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ACCESS_USERS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user's message with .mute"
        )
        return

    target_id = update.message.reply_to_message.from_user.id

    MUTED_USERS.add(target_id)

    await update.message.reply_text(
        "🔇 User muted"
    )


# .unmute
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ACCESS_USERS:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user's message with .unmute"
        )
        return

    target_id = update.message.reply_to_message.from_user.id

    MUTED_USERS.discard(target_id)

    await update.message.reply_text(
        "🔊 User unmuted"
    )


# Delete muted user's messages
async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id

        if user_id in MUTED_USERS:
            await update.message.delete()

    except:
        pass


def main():
    app = Application.builder().token(TOKEN).build()

    # Add access
    app.add_handler(
        CommandHandler("add", add_user)
    )

    # Remove access
    app.add_handler(
        CommandHandler("del", del_user)
    )

    # .mute
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^\.mute$"),
            mute
        )
    )

    # .unmute
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r"^\.unmute$"),
            unmute
        )
    )

    # Delete messages
    app.add_handler(
        MessageHandler(
            filters.ALL,
            delete_messages
        )
    )

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
