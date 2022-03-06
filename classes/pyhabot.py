import json
import time
import asyncio
import urllib
import requests
import classes.commandhandler as commands
import classes.databank as databank
import classes.scraper as scraper


class Pyhabot():
    integration = False
    scrapeTask  = False

    def __init__(self):
        config = databank.load("config.json", True)
        self.prefix   = config.get("commands_prefix", "!")
        self.interval = config.get("refresh_interval", 60)

        viewers = databank.load("viewers.json", True)
        self.viewers = {
            "AI":   viewers.get("AI", 0),
            "list": viewers.get("list", {})
        }

    def setIntegration(self, integration):
        self.integration = integration
        integration.run()

    async def onMessage(self, **kwargs):
        await commands.handler(kwargs)

    def saveSettings(self):
        return databank.save("config.json", {
            "commands_prefix":  self.prefix,
            "refresh_interval": self.interval
        }, True)

    def saveViewers(self):
        return databank.save("viewers.json", self.viewers, True)

    def startScrapeTask(self):
        if self.scrapeTask:
            self.scrapeTask.cancel()

        loop = asyncio.get_event_loop()
        self.scrapeTask = loop.create_task(self.scrapeAds())

    async def scrapeAds(self):
        # await asyncio.sleep(2)
        news = 0
        for id_ in self.viewers["list"]:
            viewer   = self.viewers["list"][id_]
            lastseen = viewer["lastseen"] if "lastseen" in viewer else False

            if "notifyon" in viewer:
                data = scraper.scrape(viewer["url"])

                if not data:
                    continue

                for ad in data["ads"]:
                    adid = int(ad["id"])

                    if lastseen == False or adid > lastseen:
                        if not self.viewers["list"][id_]["lastseen"] or adid > self.viewers["list"][id_]["lastseen"]:
                            self.viewers["list"][id_]["lastseen"] = adid

                        if type(lastseen).__name__ == "int":
                            news += 1
                            await self.sendNotification(viewer, ad)

        print(f"Scraping . . .  {news} new ads")
        self.saveViewers()

        await asyncio.sleep(self.interval)
        await self.scrapeAds()

    async def sendNotification(self, viewer, ad):
        notifyon = viewer["notifyon"]
        
        params   = commands.getURLParams(viewer["url"])
        stext    = params["stext"][0] if "stext" in params else "?"
        minprice = params["minprice"][0] if "minprice" in params else "0"
        maxprice = params["maxprice"][0] if "maxprice" in params else "∞"

        str_  = f"**{stext}**\n"
        str_ += f"{minprice} - {maxprice} Ft\n\n"
        # str_ += f"[{ad['name']}]({ad['link']})\n"
        str_ += f"[{ad['name']}]({ad['link']})\n"
        # str_ += f"**- {ad['price']} Ft** ({ad['city']}) ({ad['date']}) ([{ad['seller_name']}]({ad['seller_url']}) ({ad['seller_rates']}))"
        str_ += f"**{ad['price']} Ft** ({ad['city']}) ({ad['date']}) ({ad['seller_name']} {ad['seller_rates']})"

        if notifyon["on"] == "integration":
            if self.integration.type_ != notifyon["integration"]:
                print(f"Tried to send notification (id: {notifyon['id']}) to '{notifyon['integration']}', but failed because bot started with {self.integration.type_} integration.'")

            return await self.integration.sendMessageToChannelByID(notifyon["id"], str_)

        elif notifyon["on"] == "webhook":
            # parsed_url = urllib.parse.urlparse(notifyon["url"])
            
            # if parsed_url.netloc == "discord.com":
            requests.post(notifyon["url"], [("username", "pyhabot"), ("avatar_url", "https://i.imgur.com/kr1coKh.png"), ("content", str_)])

        return False

    def addViewer(self, url):
        self.viewers["AI"] += 1
        self.viewers["list"][ str(self.viewers["AI"]) ] = {
            "url":      url,
            "lastseen": False,
            "notifyon": False
        }
        self.saveViewers()
        return self.viewers["AI"]

    def delViewer(self, id_):
        del self.viewers["list"][str(id_)]
        self.saveViewers()
        return True

    def setViewerURL(self, id_, url):
        self.viewers["list"][str(id_)]["url"] = url
        self.saveViewers()
        return True

    def setViewerNotifyon(self, id_, type_, kwargs):
        integration = kwargs.get("integration")
        ctx         = kwargs.get("ctx")
        text        = kwargs.get("text")
        notifyon    = False

        if type_ == "here":
            notifyon = { "on": "integration", "integration": integration.type_, "id": integration.getMessageChannelID(ctx) }
        
        elif type_ == "webhook":
            args = text.strip().split()
            url  = args[3]
            notifyon = { "on": "webhook", "url": url }
        
        self.viewers["list"][str(id_)]["notifyon"] = notifyon
        self.saveViewers()
        return notifyon

bot = Pyhabot()