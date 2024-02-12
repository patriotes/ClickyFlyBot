import os
import datetime
import aiohttp
import ssl
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

bot = Client('clickyfly bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        text=f"**Bonjour {message.chat.first_name}!** \n\nCeci est le bot **ClickyFly URL Shorter**. Envoyez-moi n'importe quel lien long et obtenez un lien raccourci.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Chaîne de mises à jour des bots', url='https://t.me/Discovery_Updates')
                ],
                [
                    InlineKeyboardButton('Groupe de support', url='https://t.me/linux_repo')
                ]
            ]
        )
    )


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(
            text=f"Voici votre lien raccourci : {short_link}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Ouvrir le lien', url=short_link)
                    ]
                ]
            ),
            quote=True
        )
    except Exception as e:
        await message.reply(f'Erreur : {e}', quote=True)

async def get_shortlink(link):
    url = 'https://clickyfly.in/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, ssl=ssl.create_default_context(), raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
