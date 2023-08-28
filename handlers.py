import aiogram
from loader import dp
from services import ChatGPTService


@dp.message_handler(commands='start')
async def start(message: aiogram.types.Message):
    await message.answer('Напиши любое сообщение, чтобы начать '
                         'работу с ChatGPT.')


@dp.message_handler(commands='stream')
async def switch_stream_mode(message: aiogram.types.Message,
                             state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as state_data:
        current_stream_mode = state_data.get('stream', True)
        state_data['stream'] = not current_stream_mode
        new_mode = 'отключен' if current_stream_mode else 'включен'
        await message.answer(f'Стриминг {new_mode}.')


@dp.message_handler(lambda m: not m.is_command(), content_types='text')
async def create_chat_completion(message: aiogram.types.Message,
                                 state: aiogram.dispatcher.FSMContext):
    state_data = await state.get_data()
    chatgpt = ChatGPTService()
    await chatgpt.complete(
        message=message,
        stream=state_data.setdefault('stream', True)
        )
