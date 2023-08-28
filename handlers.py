import aiogram
from loader import dp
from services import ChatGPTService


@dp.message_handler(commands='start')
async def start(message: aiogram.types.Message):
    await message.answer('Напиши любое сообщение, чтобы начать '
                         'работу с ChatGPT.')


@dp.message_handler(lambda m: not m.is_command(), content_types='text')
async def create_chat_completion(message: aiogram.types.Message):
    chatgpt = ChatGPTService()
    await chatgpt.complete(
        message=message,
        # For streamed response
        # (slower due to Telegram Flood restriction)
        # stream=True
        )
