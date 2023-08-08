import asyncio
import telegram 

telegram_token = 'kjhaeiedpike-sjfjlkn-ljgavafafkaa-ba783'
user_id = '123456789'

async def send_telegram_message():
    bot = telegram.Bot(token=telegram_token)
    await bot.send_message(chat_id=user_id, text='Elon is active!')

async def main():
    await send_telegram_message()

if __name__ == "__main__":
    asyncio.run(main())

