import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import BOT_TOKEN

bot = aiogram.Bot(token=BOT_TOKEN,
                  parse_mode=aiogram.types.ParseMode.MARKDOWN)
dp = aiogram.Dispatcher(bot=bot, storage=MemoryStorage())
