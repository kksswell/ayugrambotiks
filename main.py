import os
print("TOKEN =", repr(os.getenv("TOKEN")))
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("TOKEN")  # токен берём из переменной окружения

WEBHOOK_HOST = "https://paramount-unplanned-celery.ngrok-free.dev"  # твой ngrok-домен
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer("Webhook работает! 🔥")


@dp.message()
async def echo(msg: Message):
    await msg.answer(f"Ты написал: {msg.text}")


async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()


def main():
    app = web.Application()

    SimpleRequestHandler(dp, bot).register(app, path=WEBHOOK_PATH)

    # ВАЖНО: в aiogram 3.7 setup_application принимает ТОЛЬКО (app, dp)
    setup_application(app, dp)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
