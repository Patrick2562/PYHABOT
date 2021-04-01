import classes.commandhandler as commands
import classes.databank as databank


class Pyhabot():
    def __init__(self):
        data = databank.load("config.json", True)
        self.prefix   = data.get("commands_prefix", "!")
        self.interval = data.get("refresh_interval", 60)

    def saveSettings(self):
        return databank.save("config.json", {
            "commands_prefix":  self.prefix,
            "refresh_interval": self.interval
        }, True)

    async def onMessage(self, **kwargs):
        await commands.handler(kwargs)


bot = Pyhabot()