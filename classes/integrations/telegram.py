import re
import requests
import marko
import telegrampy
from telegrampy.ext import commands
from classes.integration import Integration
from classes.pyhabot import bot


class Client():
    client      = False
    integration = False
    
    def __init__(self, token, integration):
        self.token       = token
        self.integration = integration
        self.client      = commands.Bot(token)

        @self.client.event
        async def on_message(message):
            await bot.onMessage(integration=self.integration, ctx=message, text=message.content)

    def run(self):
        bot.startScrapeTask()
        self.client.run()


class TelegramIntegration(Integration):
    client = False

    def __init__(self, token):
        super().__init__("telegram")
        self.client = Client(token, self)

    def run(self):
        self.client.run()

    def splitToChunks(self, text, size=4000):
        return super().splitToChunks(re.escape(text).replace("!", "\!"), size)

    async def sendMessage(self, ctx, text):
        for chunk in self.splitToChunks(text):
            await ctx.chat.send(chunk, parse_mode="MarkdownV2")

    async def reply(self, ctx, text):
        for chunk in self.splitToChunks(text):
            await ctx.reply(chunk, parse_mode="MarkdownV2")

    def getMessageChannelID(self, ctx):
        return ctx.chat.id

    async def sendMessageToChannelByID(self, id_, text):
        for chunk in super().splitToChunks(text):
            try:
                requests.get(f"https://api.telegram.org/bot{self.client.token}/sendMessage?chat_id={id_}&text={chunk}&parse_mode=Markdown")

            except Exception as err:
                print(err)


def init(token):
    bot.setIntegration( TelegramIntegration(token) )