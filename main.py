from aiogram import Bot,Dispatcher,types,executor

from api import getDefinitions
from googletrans import Translator

translator = Translator()

BOT_TOKEN = 'Token here'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def first_message(message:types.Message):
    await message.answer("Assalomu alaykum")

@dp.message_handler(content_types='text')
async def tarjimon(message:types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) >= 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translator.translate(message.text,dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id=translator.translate(message.text,dest='en').text 
        
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi!")
           

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)