from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print('Бот запущен и это отражается в командной строке')


from handlers import callback_handler, message_handler

callback_handler.register_callback_handler(dp)
message_handler.register_message_handler(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
