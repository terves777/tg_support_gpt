import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession

import config
from ai_service import generate_support_reply

session = None
if config.PROXY_URL:
    session = AiohttpSession(proxy=config.PROXY_URL)

bot = Bot(token=config.BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}! 👋\n"
        "Я виртуальный консультант службы поддержки.\n"
        "Задайте мне любой интересующий вас вопрос, и я помогу разобраться!"
    )

@dp.message(F.text)
async def handle_user_question(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    answer = await generate_support_reply(message.text)
    
    await message.answer(answer)

async def main():
    print(">>> Запущен ИИ-консультант поддержки...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())