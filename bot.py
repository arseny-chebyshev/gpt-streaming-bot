import os
import logging

import aiogram
import openai
import dotenv
dotenv.load_dotenv()

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
openai.api_key = OPENAI_TOKEN

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start(message: aiogram.types.Message):
    await message.answer('Напиши любое сообщение, чтобы начать '
                         'говорить с ChatGPT.')


@dp.message_handler(lambda m: not m.is_command())
async def create_chat_completion(message: aiogram.types.Message):
    initial_message = await message.answer('...')
    await message.answer_chat_action(aiogram.types.ChatActions.TYPING)

    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
                {
                 "role": "user",
                 "content": message.text
                }
            ],
        stream=True
    )
    message_text = ''
    async for chunk in completion:
        await message.answer_chat_action(aiogram.types.ChatActions.TYPING)
        content = chunk.choices[0].delta.get('content', None)
        if not content:
            continue
        message_text += content
        await initial_message.edit_text(message_text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    aiogram.executor.start_polling(dispatcher=dp)
