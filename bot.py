import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Load environment variables from .env file
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

# Validate critical environment variables
if not BOT_TOKEN:
    raise ValueError("Missing BOT_TOKEN in environment variables.")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# System prompt defining Joshua AI's personality and rules
SYSTEM_PROMPT = (
    "You are Joshua AI, a friendly, accurate, and helpful assistant created by Joshua. "
    "Your goal is to assist people with coding, homework, writing, translations, business ideas, "
    "and everyday questions. Explain things simply, answer naturally like a real assistant, "
    "and never pretend to know something you don't. Support Markdown formatting in your responses."
)


def get_user_history(context: ContextTypes.DEFAULT_TYPE) -> list:
    """Retrieves or initializes the conversation session history for a user."""
    if "history" not in context.user_data:
        context.user_data["history"] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return context.user_data["history"]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user_name = update.effective_user.first_name or "there"
    welcome_message = (
        f"Hello {user_name}! I am **Joshua AI**, your personal assistant.\n\n"
        "Feel free to ask me questions, request help with coding, writing, or business ideas. "
        "Use /help to see what I can do!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Start interacting with Joshua AI\n"
        "/help - Show this help message\n"
        "/about - Learn more about who created me\n\n"
        "Just send me any text message, and I'll be happy to help!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /about command."""
    about_text = (
        "I was created by Joshua to help people with coding, homework, writing, "
        "translations, business ideas, and everyday questions."
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages, queries OpenAI, and returns a response."""
    # Ignore messages without text
    if not update.message or not update.message.text:
        await update.message.reply_text("Please send a text message so I can assist you.")
        return

    user_text = update.message.text
    chat_id = update.effective_chat.id

    logger.info(f"Received message from user {update.effective_user.id}: {user_text}")

    try:
        # Show "typing..." status while generating the response
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT) # Fallback / standard typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        # Get session conversation history
        history = get_user_history(context)
        history.append({"role": "user", "content": user_text})

        # Request response from OpenAI using the current Responses API structure
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=history,
        )

        # Extract reply text (adjusting safely to response structure)
        reply_text = response.output_text

        # Append assistant response to history
        history.append({"role": "assistant", "content": reply_text})

        # Send response back to the user with Markdown support
        await update.message.reply_text(reply_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        # Graceful error handling for the user
        await update.message.reply_text(
            "I encountered an unexpected error while processing your request. Please try again later."
        )


def main() -> None:
    """Start the bot."""
    # Build the Telegram Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Register message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Joshua AI is starting up...")
    application.run_polling()


if __name__ == "__main__":
    main()
