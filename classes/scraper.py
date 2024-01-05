import traceback
import re
import requests
import urllib
from bs4 import BeautifulSoup


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

def scrapeAds(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        parsed_url = urllib.parse.urlparse(url)
        base_url   = parsed_url.scheme +'://'+ parsed_url.netloc

        html     = BeautifulSoup(response.text, "html.parser")
        uad_list = html.find("div", class_="uad-list")

        if uad_list.ul and uad_list.ul.li:
            total = int(re.findall("(\d+)", uad_list.ul.li.h3.text)[0])
            ads   = []

            if total > 0:
                medias = html.findAll(class_="media")
                
                for ad in medias:
                    title = ad.find("div", class_="uad-title")
                    info  = ad.find("div", class_="uad-info")
                    misc  = ad.find("div", class_="uad-misc")

                    if title and info:
                        info_divs = info.findAll("div")
                        misc_divs = misc.findAll("div")

                        if len(info_divs) >= 3 and len(misc_divs) >= 2:
                            ads.append({
                                "id":           ad["data-uadid"],
                                "name":         title.h1.a.text.strip(),
                                "link":         title.h1.a["href"],
                                "price":        info_divs[0].text.strip(),
                                "city":         info_divs[1].text.strip(),
                                "date":         info_divs[2].text.strip(),
                                "seller_name":  misc_divs[0].a.text.strip(),
                                "seller_url":   base_url + misc_divs[0].a["href"],
                                "seller_rates": misc_divs[1].span.text.strip(),
                                "image":        base_url + ad.a.img["src"]
                            })

            return {
                "total": total,
                "ads":   ads
            }

    except Exception as err:
        print(f'Exception: {err}')

    return False
