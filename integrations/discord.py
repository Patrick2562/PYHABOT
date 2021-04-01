import discord
import integrations.Parent as IntegrationsParent
import classes.pyhabot as pyhabot


class Client(discord.Client):
    integration = False

    def __init__(self, token, integration):
        self.integration = integration
        super().__init__()

    async def on_message(self, message):
        if not message.author.bot:
            await pyhabot.bot.onMessage(integration=self.integration, ctx=message, text=message.content)


class Integration(IntegrationsParent.Parent):
    client = False

    def __init__(self, token):
        super().__init__("Discord")
        self.client = Client(token, self)
        self.client.run(token)

    async def sendMessage(self, ctx, text):
        for chunk in self.splitToChunks(text, size=2000):
            await ctx.channel.send(chunk)

    async def reply(self, ctx, text):
        for chunk in self.splitToChunks(text, size=2000):
            await ctx.reply(chunk, mention_author=True)


def init(token):
    Integration(token)