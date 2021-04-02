from dotenv import dotenv_values
config = dotenv_values(".env")

import json
import urllib
import classes.pyhabot as pyhabot
import classes.scraper as scraper


def isCommand(text):
    return text and len(text) > 1 and text[0] == pyhabot.bot.prefix
        
def argsCheck(args, expected):
    # for arg in args:
    return True

def getURLParams(url):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(parsed_url.query)

async def handler(kwargs):
    integration = kwargs.get("integration")
    ctx         = kwargs.get("ctx")
    text        = kwargs.get("text")
    
    if not isCommand(text):
        return False

    args = text.strip().split()
    cmd  = args.pop(0)[1:]

    if cmd == "help":
        str_  = f"{pyhabot.bot.prefix}help        | Listázza az elérhető parancsokat.\n"
        str_ += f"{pyhabot.bot.prefix}settings    | Megmutatja a bot beállításait.\n"
        str_ += f"{pyhabot.bot.prefix}add         | Felvenni lehet vele egy új hirdetésfigyelőt.\n"
        str_ += f"{pyhabot.bot.prefix}del         | Törölni lehet vele egy létező hirdetésfigyelőt.\n"
        str_ += f"{pyhabot.bot.prefix}list        | Listázza a felvett hirdetésfigyelőket.\n"
        str_ += f"{pyhabot.bot.prefix}info        | Meglehet vele nézni egy hirdetésfigyelő adatait.\n"
        str_ += f"{pyhabot.bot.prefix}notifyon    | Módosítani lehet vele, hogy hová küldje az értesítéseket egy adott hirdetésfigyelő.\n"
        str_ += f"{pyhabot.bot.prefix}rescrape    | Elfelejti az eddig átvizsgált hirdetéseket, ismételten átnézi az összeset és elküldi az értesítéseket.\n"
        str_ += f"{pyhabot.bot.prefix}seturl      | Módosítani lehet egy hirdetésfigyelő URL-jét.\n"
        str_ += f"{pyhabot.bot.prefix}setprefix   | Módosítani lehet vele a parancs prefixet.\n"
        str_ += f"{pyhabot.bot.prefix}setinterval | Belehet vele állítani hány másodpercenként ellenőrizzen.\n"
        str_ += f"{pyhabot.bot.prefix}getraw      | Elküldi a scrapelt hirdetések adatait json formátumban."

        await integration.sendMessage(ctx, f"```\n{str_}\n```")

    elif cmd == "settings":
        str_  = f"- Integration: {pyhabot.bot.integration.type_}\n"
        str_ += f"- Commands prefix: {pyhabot.bot.prefix}\n"
        str_ += f"- Refresh interval: {pyhabot.bot.interval} sec"
        await integration.sendMessage(ctx, f"```\n{str_}\n```")

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
        pyhabot.bot.startScrapeTask()
        pyhabot.bot.saveSettings()
        await integration.sendMessage(ctx, f"Refresh interval módosítva: `{interval} sec`")

    elif cmd == "add":
        url = args[0]

        id_ = pyhabot.bot.addViewer(url)
        if id_:
            pyhabot.bot.setViewerNotifyon(id_, "here", kwargs)
            await integration.sendMessage(ctx, f"Sikeresen hozzáadva! - `ID: {id_}`")

    elif cmd == "del":
        id_ = args[0]

        if pyhabot.bot.delViewer(id_):
            await integration.sendMessage(ctx, f"Sikeresen törölve! - `ID: {id_}`")

    elif cmd == "list":
        str_ = ""

        for id_ in pyhabot.bot.viewers["list"]:
            viewer = pyhabot.bot.viewers["list"][id_]
            params = getURLParams(viewer["url"])

            str_ += ('\n' if str_ != '' else '') + f"`ID: {id_}` - " + params["stext"][0]

        await integration.sendMessage(ctx, str_ if str_ != "" else "Nincs még felvett hirdetésfigyelő!") 

    elif cmd == "info":
        id_ = args[0]

        viewer = pyhabot.bot.viewers["list"][id_]
        params = getURLParams(viewer["url"])

        stext    = params["stext"][0] if "stext" in params else "?"
        minprice = params["minprice"][0] if "minprice" in params else "0"
        maxprice = params["maxprice"][0] if "maxprice" in params else "∞"

        str_  = f"- ID: {id_}\n"
        str_ += f"- Search for: {stext}\n"
        str_ += f"- Price limit: {minprice} - {maxprice} Forint\n"
        str_ += f"- Notify on: {viewer['notifyon']['integration'] if 'integration' in viewer['notifyon'] else 'webhook'}\n"
        str_ += f"- URL: {viewer['url']}"
        await integration.sendMessage(ctx, f"```\n{str_}\n```")

    elif cmd == "seturl":
        id_ = args[0]
        url = args[1]

        if pyhabot.bot.setViewerURL(id_, url):
            params = getURLParams(url)
            await integration.sendMessage(ctx, f"URL módosítva! - `ID: {id_}` - " + params["stext"][0])

    elif cmd == "notifyon":
        id_   = args[0]
        type_ = args[1]

        notifyon = pyhabot.bot.setViewerNotifyon(id_, type_, kwargs)
        if notifyon:
            await integration.sendMessage(ctx, f"Értesítés típusa beálltva! - `ID: {id_}` - " + (notifyon["integration"] if "integration" in notifyon else "webhook"))

    elif cmd == "rescrape":
        for id_ in pyhabot.bot.viewers["list"]:
            pyhabot.bot.viewers["list"][id_]["lastseen"] = 0

        pyhabot.bot.startScrapeTask()
        await integration.sendMessage(ctx, f"Minden hirdetés újbóli átvizsgálása...")


    return False