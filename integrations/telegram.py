import re
import requests
import marko
import telegrampy
from telegrampy.ext import commands
import integrations.Parent as IntegrationsParent
import classes.pyhabot as pyhabot


class Client():
    client      = False
    integration = False
    
    def __init__(self, token, integration):
        self.token       = token
        self.integration = integration
        self.client      = commands.Bot(token)

        @self.client.event
        async def on_message(message):
            await pyhabot.bot.onMessage(integration=self.integration, ctx=message, text=message.content)

    def run(self):
        self.client.run()


class Integration(IntegrationsParent.Parent):
    client = False
    type_  = "Telegram"

    def __init__(self, token):
        super().__init__("Telegram")
        self.client = Client(token, self)

    def run(self):
        self.client.run()

    def splitToChunks(self, text, size=2000):
        return super().splitToChunks(re.escape(text).replace("!", "\!"), size)

    async def sendMessage(self, ctx, text):
        for chunk in self.splitToChunks(text, 4000):
            await ctx.chat.send(chunk, parse_mode="MarkdownV2")

    async def reply(self, ctx, text):
        for chunk in self.splitToChunks(text, 4000):
            await ctx.reply(chunk, parse_mode="MarkdownV2")

    def getMessageChannelID(self, ctx):
        return ctx.chat.id

    async def sendMessageToChannelByID(self, id_, text):
        #try:
        #    print(await commands.ChatConverter().convert(self.client, id_))
        #except Exception as err:
        #    print(err)

        #if chat:

        for chunk in super().splitToChunks(text, 4000):
            # await chat.send(chunk, parse_mode="MarkdownV2")
            try:
                requests.get(f"https://api.telegram.org/bot{self.client.token}/sendMessage?chat_id={id_}&text={chunk}&parse_mode=Markdown")
            except Exception as err:
                print(err)

def init(token):
    pyhabot.bot.setIntegration( Integration(token) )