import json
import classes.scraper as scraper

class Pyhabot():
    def __init__(self):
        pass

    def isCommand(self, cmd):
        return cmd and len(cmd) > 1 and cmd[0] == '!'

    async def commandHandler(self, **kwargs):
        integration = kwargs.get("integration")
        ctx         = kwargs.get("ctx")
        text        = kwargs.get("text")
        
        if not self.isCommand(text):
            return False

        args = text.strip().split()
        cmd  = args.pop(0)[1:]

        if cmd == "raw":
            data = scraper.scrape(args[0])
            await integration.sendMessage(ctx, json.dumps(data))

    async def onMessage(self, **kwargs):
        await self.commandHandler(**kwargs)


bot = Pyhabot()