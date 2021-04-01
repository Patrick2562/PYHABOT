from dotenv import dotenv_values
config = dotenv_values(".env")

import json
import classes.pyhabot as pyhabot
import classes.scraper as scraper


def isCommand(text):
    return text and len(text) > 1 and text[0] == pyhabot.bot.prefix
        
def argsCheck(args, expected):
    # for arg in args:
    return True

async def handler(kwargs):
    integration = kwargs.get("integration")
    ctx         = kwargs.get("ctx")
    text        = kwargs.get("text")
    
    if not isCommand(text):
        return False

    args = text.strip().split()
    cmd  = args.pop(0)[1:]

    if cmd == "info":
        str_  = f"\- Commands prefix: `{pyhabot.bot.prefix}`\n"
        str_ += f"\- Refresh interval: `{pyhabot.bot.interval} sec`"
        await integration.sendMessage(ctx, str_)

    elif cmd == "getraw":
        data = scraper.scrape(args[0])
        await integration.sendMessage(ctx, json.dumps(data))
        return True

    elif cmd == "setprefix":
        if not argsCheck(args, ["Integer"]):
            return False

        prefix = str(args[0])

        pyhabot.bot.prefix = prefix
        pyhabot.bot.saveSettings()
        await integration.sendMessage(ctx, f"Prefix módosítva: `{prefix}`")

    elif cmd == "setinterval":
        if not argsCheck(args, ["Integer"]):
            return False

        interval = int(args[0])

        pyhabot.bot.interval = interval
        pyhabot.bot.saveSettings()
        await integration.sendMessage(ctx, f"Refresh interval módosítva: `{interval}`")

    return False