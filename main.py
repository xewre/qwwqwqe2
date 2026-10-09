```python
import os
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")
LOLZ_API_TOKEN = os.getenv("LOLZ_API_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💰 Баланс Lolzteam",
        callback_data="lolz_balance"
    )
    return builder.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\nНажми кнопку ниже, чтобы посмотреть баланс Lolzteam.",
        reply_markup=main_keyboard()
    )


@dp.callback_query(F.data == "lolz_balance")
async def show_balance(callback: CallbackQuery):
    await callback.answer()

    if not LOLZ_API_TOKEN:
        await callback.message.answer("❌ Не настроен LOLZ_API_TOKEN.")
        return

    headers = {
        "Authorization": f"Bearer {LOLZ_API_TOKEN}"
    }

    url = "https://api.lzt.market/balance/exchange"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:

                data = await response.json(content_type=None)

                if response.status != 200:
                    await callback.message.answer(
                        f"❌ Ошибка API: HTTP {response.status}"
                    )
                    return

                await callback.message.answer(
                    "💰 Ответ Lolzteam API:\n\n"
                    f"<pre>{str(data)[:3500]}</pre>",
                    parse_mode="HTML",
                    reply_markup=main_keyboard()
                )

    except Exception:
        await callback.message.answer(
            "❌ Не удалось получить баланс. Проверь токен и подключение."
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```