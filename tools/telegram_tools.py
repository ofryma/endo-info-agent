import os
import asyncio
from typing import Optional

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from langchain_core.tools import Tool, tool
from colorama import Fore, Back, Style

from tools import tools_memory

# Load environment variables
load_dotenv()

# Get Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_GROUP_ID')

async def send_message_async(input: str):

    # Initialize the bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Send the message to the specified chat ID (group)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=input)

    # Close the bot instance
    await bot.close()


@tool
def send_telegram_message(input: str) -> str:
    """
    Send a message to telegram group.
    
    Args:
        input (str): The message to send
        
    Returns:
        str: Status message indicating success or failure
    """
    if not TELEGRAM_BOT_TOKEN:
        return "Error: TELEGRAM_TOKEN environment variable is not set"
    
    if not TELEGRAM_CHAT_ID:
        return "Error: TELEGRAM_GROUP_ID environment variable is not set"

    message_content = tools_memory.memory.recall(tools_memory.ToolMemoryKeys.TELEGRAM_MESSAGE_CONTENT.value)

    try:
        
        # Create event loop and run async function
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_message_async(message_content))
        
        return f"Successfully sent message to Telegram group"
        
    except TelegramError as e:
        error_message = f"Failed to send Telegram message: {str(e)}"
        print(Fore.RED + error_message + Style.RESET_ALL)
        return error_message
    except Exception as e:
        error_message = f"Unexpected error while sending Telegram message: {str(e)}"
        print(Fore.RED + error_message + Style.RESET_ALL)
        return error_message


if __name__ == "__main__":
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

    async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        print(update.effective_chat.id)

        await update.message.reply_text(f'Chat ID: {update.effective_chat.id}')

    # Change the api key to the one recived from botfather
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

    app.add_handler(CommandHandler("hello", hello))

    print("Start polling")
    app.run_polling()