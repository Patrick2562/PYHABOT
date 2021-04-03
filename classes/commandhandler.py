from dotenv import dotenv_values
config = dotenv_values(".env")

import json
import urllib
import requests
import classes.pyhabot as pyhabot
import classes.scraper as scraper


def isCommand(text):
    return text and len(text) > 1 and text[0] == pyhabot.bot.prefix

def canbeInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def argsCheck(args, expected, howtouse):
    if len(args) < len(expected):
        raise Exception(f"Missing arguments, {len(expected)} required, got {len(args)}.\n**USE:** `{howtouse}`")

    i = 0
    for exp in expected:
        arg = int(args[i]) if (exp == "int" and canbeInt(args[i])) else args[i]
        if type(arg).__name__ != exp:
            raise Exception(f"Expected '{exp}' at argument {i}, got '{type(arg).__name__}'.\n**USE:** `{howtouse}`")
        i += 1

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

    try:
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
            argsCheck(args, ["str"], f"{pyhabot.bot.prefix}{cmd} <url>")

            if not "PASTEBIN_API_KEY" in config or not config["PASTEBIN_API_KEY"] or config["PASTEBIN_API_KEY"] == "False":
                return await integration.sendMessage(ctx, "Nem használható, mert nincs megadva 'PASTEBIN_API_KEY' a **.env** config fájlban!")

            data = scraper.scrape(args[0])
            response = requests.post("https://pastebin.com/api/api_post.php", [
                ("api_dev_key", config["PASTEBIN_API_KEY"]),
                ("api_paste_format", "json"),
                ("api_option", "paste"),
                ("api_paste_code", json.dumps(data, indent=4, sort_keys=True))
            ])
            await integration.sendMessage(ctx, "Link: " + response.text)
            return True

        elif cmd == "setprefix":
            argsCheck(args, ["str"], f"{pyhabot.bot.prefix}{cmd} <prefix>")

            prefix = str(args[0])

            pyhabot.bot.prefix = prefix
            pyhabot.bot.saveSettings()
            await integration.sendMessage(ctx, f"Prefix módosítva: `{prefix}`")

        elif cmd == "setinterval":
            argsCheck(args, ["int"], f"{pyhabot.bot.prefix}{cmd} <sec>")

            interval = int(args[0])

            pyhabot.bot.interval = interval
            pyhabot.bot.startScrapeTask()
            pyhabot.bot.saveSettings()
            await integration.sendMessage(ctx, f"Refresh interval módosítva: `{interval} sec`")

        elif cmd == "add":
            argsCheck(args, ["str"], f"{pyhabot.bot.prefix}{cmd} <url>")

            url = args[0]

            id_ = pyhabot.bot.addViewer(url)
            if id_:
                pyhabot.bot.setViewerNotifyon(id_, "here", kwargs)
                await integration.sendMessage(ctx, f"Sikeresen hozzáadva! - `ID: {id_}`")

        elif cmd == "del":
            argsCheck(args, ["int"], f"{pyhabot.bot.prefix}{cmd} <id>")

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
            argsCheck(args, ["int"], f"{pyhabot.bot.prefix}{cmd} <id>")

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
            argsCheck(args, ["int", "str"], f"{pyhabot.bot.prefix}{cmd} <id> <url>")

            id_ = args[0]
            url = args[1]

            if pyhabot.bot.setViewerURL(id_, url):
                params = getURLParams(url)
                await integration.sendMessage(ctx, f"URL módosítva! - `ID: {id_}` - " + params["stext"][0])

        elif cmd == "notifyon":
            argsCheck(args, ["int", "str"], f"{pyhabot.bot.prefix}{cmd} <id> <here / webhook> [<webhook url>]")

            id_   = args[0]
            type_ = args[1]

            notifyon = pyhabot.bot.setViewerNotifyon(id_, type_, kwargs)
            if notifyon:
                await integration.sendMessage(ctx, f"Értesítés típusa beálltva! - `ID: {id_}` - " + (notifyon["integration"] if "integration" in notifyon else "webhook"))

        elif cmd == "rescrape":
            for id_ in pyhabot.bot.viewers["list"]:
                pyhabot.bot.viewers["list"][id_]["lastseen"] = 0

            await integration.sendMessage(ctx, f"Minden hirdetés újbóli átvizsgálása...")
            pyhabot.bot.startScrapeTask()

    except Exception as err:
        await integration.sendMessage(ctx, str(err))

    return False