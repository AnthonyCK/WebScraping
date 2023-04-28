import requests 
import pandas as pd
from bs4 import BeautifulSoup
import constants


def fetch_data(category_1, category_2):
    products = []
    url = constants.URL + f"/static/{category_1}/{category_2}.html"
    # category_1 = "computers"
    # category_2 = "laptops"
    while True:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            log.append({"url":url, "message": "Success"})

            for anchor in soup.find_all("a", class_="title"): 
                product_url = anchor.get("href")
                if product_url:
                    # If the URL is relative, join it with the base URL
                    if not product_url.startswith("http"):
                        product_url = f"http://di75wax.devweb.mwn.de/static{product_url.replace('..', '')}"
                    products.append({"L1": category_1, "L2": category_2, "url": product_url})

            # Get the URL of the next page
            next_page = soup.find_all("a", {"rel": "next"})
            if next_page:
                # If the URL is relative, join it with the base URL
                next_page = next_page[0].get("href")
                if not next_page.startswith("http"):
                    next_page = f"http://di75wax.devweb.mwn.de/static/{category_1}/{next_page}"
                url = next_page
            else:
                break
        except:
            log.append({"url":url, "message": "Fail: " + response.status_code})

    for item in products:
        try:
            page = requests.get(item['url'])
            file_path = f"{constants.FOLDER_PATH}/{item['L1']}/{item['L2']}/"
            with open(file_path + item['url'].split("/")[-1], 'wb+') as f:
                f.write(page.content)
            log.append({"url":item['url'], "message": "Success"})
        except:
            log.append({"url":item['url'], "message": "Fail: " + page.status_code})


if __name__ == "__main__":
    log = []
    fetch_data("computers", "laptops")
    fetch_data("computers", "tablets")
    fetch_data("phones", "touch")
    pd.DataFrame(log).to_csv(constants.LOG_CSV, sep=";", index=False)

