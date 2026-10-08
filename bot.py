import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command


from openai import AsyncOpenAI


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Не найден TELEGRAM_TOKEN")

if not OPENAI_API_KEY:
    raise RuntimeError("Не найден OPENAI_API_KEY")


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai = AsyncOpenAI(api_key=OPENAI_API_KEY)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я StarWow Bot 🤖\n"
        "Напиши мне любой вопрос — я постараюсь помочь."
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🤖 Команды:\n\n"
        "/start — запустить бота\n"
        "/help — помощь\n\n"
        "А обычные сообщения я передаю ИИ."
    )


@dp.message()
async def answer(message: types.Message):
    if not message.text:
        return

    try:
        response = await ai.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "Ты умный и дружелюбный Telegram-бот StarWow. "
                "Отвечай понятно, кратко и на языке пользователя. "
                "Если пользователь пишет по-русски — отвечай по-русски."
            ),
            input=message.text,
        )

        answer_text = response.output_text

        if not answer_text:
            answer_text = "Не получилось сформировать ответ 😕"

        await message.answer(answer_text)

    except Exception as error:
        print("Ошибка:", error)
        await message.answer(
            "Произошла ошибка при обращении к ИИ. Попробуй ещё раз."
        )


async def main():
    print("StarWow Bot запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
