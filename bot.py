import logging
import aiogram
from loader import dp
import handlers

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Hanlders loaded: {handlers}')
    aiogram.executor.start_polling(dispatcher=dp)
