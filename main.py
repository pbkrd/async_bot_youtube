from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print('Бот запущен и это отражается в командной строке')


from handlers import client, admin, other

client.register_client_handler(dp)
# admin.
other.register_other_handler(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
