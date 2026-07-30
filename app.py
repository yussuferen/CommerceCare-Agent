import os
from dotenv import load_dotenv
load_dotenv()
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent import run_agent

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"Hello {user.first_name}! I am CommerceCareAI, your intelligent customer support assistant. How can I help you today?"
    await update.message.reply_text(welcome_message)

async def agent_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Show "typing..." action while the bot is generating a response
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        agent_response = run_agent(user_message)
        await update.message.reply_text(agent_response)
        
    except Exception as e:
        logging.error(f"An error occurred during agent execution: {e}")
        await update.message.reply_text("I'm sorry, I encountered an internal error while processing your request. Please try again later.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent_message_handler))

    print("🚀 CommerceCareAI Telegram Bot has successfully started! Listening for incoming messages...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()