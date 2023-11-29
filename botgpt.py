import os
import openai
import sys
import asyncio    
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

class Reference:
    """
     A class to store response from chatGPT API
    """

    def __init__(self) -> None:
        """
        This saves the conversation context with the bot
        """
        self.response = ""


# Load enviroment variables
load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")
telegram_token = os.getenv("Bot_TOKEN")
gpt_model = os.getenv("model_NAME")


# Initialize Bot
bot = Bot(token=telegram_token)
dp = Dispatcher()

reference = Reference()

def clear_past():
    """
    This clears the current conversation context
    """
    reference.response = ""

@dp.message(CommandStart())
async def welcome(message: types.Message) -> None:
    """
    This handler receives messages with `/start`
    """
    await message.reply("Hi\nI am Botgpt!\nCreated by Julius. How can I assist you?")

# @dp.message(commands=['clear'])
# async def clear(message: types.Message):
#     """
#     This handler clears context of conversation with `/clear`
#     """
#     clear_past()
#     await message.reply("I have cleared the past conversation context")

# @dp.message(commands=['help'])
# async def helper(message: types.Message):
#     """
#     This handler to display the help menu.
#     """
#     response = """
#     Hi There, I'm chatGPT Telegram bot created by Julius! Please follow these commans -
#     /start - to start the conversation
#     /clear - to clear the past conversation
#     /help - to get this help menu
#     I hope this helps. :)
#     """
#     await message.reply(response)

@dp.message()
async def chatgpt(message: types.Message):
    """
    This handler to process the user's input and generate a response using the chatGPT API
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = gpt_model,
        messages = [
            {"role": "assistant", "content": reference.response},
            {"user": "user", "content": message.text}
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send(chat_id = message.chat.id, text = reference.response)

async def main() -> None:
    bot = Bot(telegram_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())