import json
import time
import threading
import classes.commandhandler as commands
import classes.databank as databank
import classes.scraper as scraper


class Pyhabot():
    integration = False

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

        self.timerThread = threading.Thread(target=self.scrapeAds, daemon=True)
        self.timerThread.start()

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

    def scrapeAds(self):
        print("Scraping...")
        for id_ in self.viewers["list"]:
            viewer = self.viewers["list"][id_]

            if "notifyon" in viewer:
                data = scraper.scrape(viewer["url"])

                for ad in data["ads"]:
                    adid = int(ad["id"])

                    lastseen = viewer["lastseen"] if "lastseen" in viewer else 0
                    
                    if adid > lastseen:
                        self.viewers["list"][id_]["lastseen"] = adid
                        self.sendNotification(viewer, ad)
                    
        self.saveViewers()

        time.sleep(self.interval)
        self.timerThread = threading.Thread(target=self.scrapeAds, daemon=True)
        self.timerThread.start()

    def sendNotification(self, viewer, ad):
        print(viewer["notifyon"])

    def addViewer(self, url):
        self.viewers["AI"] += 1
        self.viewers["list"][ str(self.viewers["AI"]) ] = {
            "url":      url,
            "lastseen": 0,
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
            notifyon = { integration: integration.type_, id_: integration.getMessageChannelID(ctx) }
        elif type_ == "webhook":
            args = text.strip().split()
            url  = args[0]
            notifyon = { webhook: url }
        
        self.viewers["list"][str(id_)]["notifyon"] = notifyon
        self.saveViewers()
        return notifyon

bot = Pyhabot()