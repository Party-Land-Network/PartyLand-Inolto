import os
import discord
from discord.ext import commands
import telebot

# Configurazione del bot di Discord
discord_token = 'TOKEN_DISCORD'
discord_channel_ids = {
    'update': 'DISCORD_UPDATE_CHANNEL_ID',
    'survival': 'DISCORD_SURVIVAL_CHANNEL_ID',
    'network': 'DISCORD_NETWORK_CHANNEL_ID',
    'roleplay': 'DISCORD_ROLEPLAY_CHANNEL_ID'
}

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for category, channel_id in discord_channel_ids.items():
        if message.channel.id == int(channel_id):
            # Inoltra il messaggio a Telegram
            telebot.send_message(chat_id=f'TELEGRAM_{category.upper()}_CHAT_ID', text=f"{category} - {message.author}: {message.content}")
    await bot.process_commands(message)

# Configurazione del bot di Telegram
telegram_token = 'TOKEN_TELEGRAM'

telebot = telebot.TeleBot(telegram_token)

@telebot.message_handler(commands=['start'])
def start(message):
    telebot.send_message(message.chat.id, 'Bot Telegram avviato!')

@telebot.message_handler(func=lambda message: True, content_types=['text'])
def forward_to_discord(message):
    # Estrai la categoria dal testo del messaggio Telegram
    category = message.text.split()[0].lower()

    if category in discord_channel_ids:
        # Inoltra il messaggio al canale Discord corrispondente
        bot.get_channel(int(discord_channel_ids[category])).send(f"{message.from_user.username}: {message.text[len(category)+1:]}")

if __name__ == '__main__':
    # Avvia il bot di Discord
    bot.run(discord_token)

    # Avvia il bot di Telegram
    telebot.polling()
