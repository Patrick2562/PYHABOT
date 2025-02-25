import traceback
import re
import requests
import urllib
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def getURLParams(url):
    parsed_url = urllib.parse.urlparse(url)
    return urllib.parse.parse_qs(parsed_url.query)

def scrapeCategoryName(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        html          = BeautifulSoup(response.text, "html.parser")
        category_name = html.find("div", id="top").find("ol", class_="breadcrumb").find_all("li", class_="breadcrumb-item")[-1].text
        
        return category_name or "n/a"

    except Exception as err:
        traceback.print_exc()

    return "n/a"

def convertDate(expression):
    now = datetime.now()
    if expression.startswith("ma"):
        time_part = expression.split()[1]
        ret_date = datetime.strptime(time_part, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    elif expression.startswith("tegnap"):
        time_part = expression.split()[1]
        ret_date = datetime.strptime(time_part, "%H:%M").replace(year=now.year, month=now.month, day=now.day) - timedelta(days=1)
    else:
        ret_date = datetime.strptime(expression, "%Y-%m-%d")
    return ret_date.strftime("%Y-%m-%d %H:%M")


def scrapeAds(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        parsed_url = urllib.parse.urlparse(url)
        base_url   = parsed_url.scheme +'://'+ parsed_url.netloc

        html     = BeautifulSoup(response.text, "html.parser")
        uad_list = html.find("div", class_="uad-list")

        if uad_list.ul and uad_list.ul.li:
            medias = html.findAll(class_="media")
            ads    = []
            
            for ad in medias:
                title = ad.find("div", class_="uad-col-title")
                info  = ad.find("div", class_="uad-col-info")
                price  = ad.find("div", class_="uad-price")

                if title and info:
                    new_entry = {
                        "id":           ad["data-uadid"],
                        "name":         title.h1.a.text.strip(),
                        "link":         title.h1.a["href"],
                        "price":        price.span.text.strip(),
                        "city":         info.find("div", class_="uad-cities").text.strip(),
                        "date":         convertDate(info.find("div", class_="uad-time").time.text.strip()),
                        "seller_name":  info.find("span", class_="uad-user-text").a.text.strip(),
                        "seller_url":   base_url + info.find("span", class_="uad-user-text").a["href"],
                        "seller_rates": info.find("span", class_="uad-user-text").span.text.strip(),
                        "image":        ad.a.img["src"]
                    }
                    
                    if all(new_entry.values()):
                        ads.append(new_entry)
                    else:
                        print("Invalid new ad entry:", new_entry)
                else:
                    print("Invalid ad entry:", ad)
            return ads

    except Exception as err:
        traceback.print_exc()

    return False
