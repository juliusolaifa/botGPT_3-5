import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from openai import OpenAI
from aiogram.handlers import MessageHandler


# A reference class for saving conversation context
class Reference:
    """
    A class to store previously response from the chatGPT API
    """

    def __init__(self) -> None:
        self.response = ""

    def clear(self):
        """
         A function to clear the previous conversation and context.
        """
        self.response = ""

load_dotenv()
openai_api = os.getenv("OpenAI_API_KEY")
bot_token = os.getenv("Bot_TOKEN")
gpt_model = os.getenv("Model_NAME")
dispatcher = Dispatcher()
router = Router()
reference = Reference()
bot = Bot(token=bot_token, parse_mode='HTML')
client = OpenAI()

# This helps route user defined command
def register_routers(dispatcher: Dispatcher) -> None:
    """
    Register routers
    """
    dispatcher.include_router(router)

# the help command
@router.message(Command('help'))
async def cmd_help(msg: types.Message) -> None:
    """
    A handler to display the help menu.
    """
    reply_text = """
    Please follow these commands - \n
    /start - to start the conversation
    /clear - to clear past conversations.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await msg.answer(text = reply_text)

#the clear command
@router.message(Command('clear'))
async def clear(msg: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    reference.clear()
    await msg.answer(text = "I've cleared the past conversation and context.")

#the start command
@dispatcher.message(CommandStart())
async def cmd_start(msg: types.Message) -> None:
    reply_text = f"Hello {hbold(msg.from_user.first_name)}\nI am botgpt\nCreated by Julius Olaifa\n\nI am a child of chatGPT.\nWhat can I do for you?"
    await msg.answer(text = reply_text)

#the chatgpt
@router.message()
async def gpt_response(msg: types.Message) -> None:
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{msg.text}")
    response = client.chat.completions.create(
        model = gpt_model,
        messages = [
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": msg.text}
        ]
    )
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = msg.chat.id, text = reference.response)



async def main() -> None:
    """
    Entry point
    """
    register_routers(dispatcher)
    await dispatcher.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())