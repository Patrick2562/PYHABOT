import telegrampy
from telegrampy.ext import commands
import integrations.Parent as IntegrationsParent
import classes.pyhabot as pyhabot


class Client():
    client      = False
    integration = False
    
    def __init__(self, token, integration):
        self.integration = integration
        self.client      = commands.Bot(token)

        @self.client.event
        async def on_message(message):
            await pyhabot.bot.onMessage(integration=self.integration, ctx=message, text=message.content)

    def run(self):
        self.client.run()


class Integration(IntegrationsParent.Parent):
    client  = False

    def __init__(self, token):
        super().__init__("Telegram")
        self.client = Client(token, self)
        self.client.run()

    async def sendMessage(self, ctx, text):
        for chunk in self.splitToChunks(text, size=4000):
            await ctx.chat.send(chunk)

    async def reply(self, ctx, text):
        for chunk in self.splitToChunks(text, size=4000):
            await ctx.reply(chunk)


def init(token):
    Integration(token)