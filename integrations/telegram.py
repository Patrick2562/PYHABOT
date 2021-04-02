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

    async def sendMessage(self, ctx, text):
        text = text.replace("-", "\-").replace(".", "\.")
        for chunk in self.splitToChunks(text, size=4000):
            await ctx.chat.send(chunk, parse_mode="MarkdownV2")

    async def reply(self, ctx, text):
        text = text.replace("-", "\-").replace(".", "\.")
        for chunk in self.splitToChunks(text, size=4000):
            await ctx.reply(chunk, parse_mode="MarkdownV2")

    def getMessageChannelID(self, ctx):
        return ctx.chat.id

    async def sendMessageToChannelByID(self, id_, text):
        chat = commands.Bot.get_chat(id_)
        print(chat)

        if chat:
            text = text.replace("-", "\-").replace(".", "\.")
            for chunk in self.splitToChunks(text, size=2000):
                await chat.send(chunk, parse_mode="MarkdownV2")

def init(token):
    pyhabot.bot.setIntegration( Integration(token) )