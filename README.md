# Web Scraping for Scientists

Codes for PhD. Course, Web Scraping for Scientists: An Introduction with Python.

- Python script of the web scraper
- Link: http://di75wax.devweb.mwn.de
- Scraped data as a .csv file with the following attributes for each of the 147 
products (products in lines, attributes in columns)
  1. Product ID
  2. Product category L1 (“Computer”, “Phone”)
  3. Product category L2 (“Laptop”, “Tablet”, “Touch”)
  4. Product Name
  5. Price (USD)
  6. Description
  7. Product rating (number of stars)
  8. Number of reviews
  9. Colors (if available)
  10. Storage capacity (if available)
- Scraping log of the individual URLs as a .csv file

Example Code (Felix)

# Crawling
### load necessary packages
```
import requests 
import pandas as pd

```
### Get the URL of the products in a list and create scraping log 
####Check whether the correct ULR vein interest has been used
```
log = []
products = []

for i in range(486,633):
    products.append(f'http://di75wax.devweb.mwn.de/static/product/{i}.html') 
    url = (f'http://di75wax.devweb.mwn.de/static/product/{i}.html')
    if requests.get(url).status_code == 200: 
        log.append({"url":url, "message": "Success"})
    else:
        log.append({"url":url, "message": "Fail"})  
pd.DataFrame(log).to_csv("logging.csv",sep=";", index=False)

```

# Fetching

### save products as html files

```
for i in range(0,len(products)):
    page = requests.get(products[i])
    with open(f'product_url_{i}.html', 'wb+') as f:
        f.write(page.content)
```

# Parsing

### load necessary packages

```
import re
from bs4 import BeautifulSoup as bs

```


```
variable_list = []
for i in range(0,len(products)):
    with open(f"product_url_{i}.html") as file:
        soup = bs(file, "html.parser")
        
        # Price, Name and Description 
    name_price_des = soup.find('div',  {"class":"caption"}).text
    result_1 = name_price_des.split('\n')
    result_2 = ','.join(filter(None, result_1))
    price = result_2.split(',')[0][1:]
    name = result_2.split(',')[1]
    description = soup.find('p',  {"class":"description"}).text


    # Number of reviews 
    results_3 = soup.find('div',  {"class":"ratings"}).text
    reviews = re.findall(r'\d+', results_3)

    # Product rating (Number of stars)
    results_4 = str(soup.find('div',  {"class":"ratings"}))
    stars = results_4.count('glyphicon-star')

    # Colors (if available)
    try: 
        dropdown = soup.find('div',  {"class":"dropdown"}).text
        result_5 = dropdown.split('\n')
        result_6 = ','.join(filter(None, result_5[1:]))
        result_7 = result_6.split(',')[1:]
        colors =  '/'.join(result_7)
    except: 
        colors = ""
    
    # Capacity (if available)
    try: 
        capacity = soup.findAll("button", {"type": "button"})
        capacity = "/".join([store.text for store in capacity if len(re.findall("disabled", str(store)))==0])
    except: 
        capacity = ""
        
## combine everything into a row and later save it in a loop over all observations together.
    product = {"ID": i+486, "name":name, "price":price, "description":description, "reviews":reviews[0], "stars":stars, "colors":colors, "capacity":capacity}
    variable_list.append(product)
    
# make it a dataframe
import pandas as pd
data = pd.DataFrame(variable_list)

```
### Order data

```
# Product category L1 
# 486 - 494: Phone, Touch
# 495 - 515: Computer, Tablet 
# 516 - 632:Computer, Laptop 
data.loc[(data["ID"]>=486)&(data["ID"]<495), "L1"] = "Phone"
data.loc[(data["ID"]>=495)&(data["ID"]<633), "L1"] = "Computer"

# Product category L2
data.loc[(data["ID"]>=486)&(data["ID"]<495), "L2"] = "Touch"
data.loc[(data["ID"]>=495)&(data["ID"]<516), "L2"] = "Tablet"
data.loc[(data["ID"]>=516)&(data["ID"]<633), "L2"] = "Laptop"


data = data[['ID', 'L1', 'L2', 'name', 'price', 'description', 'stars', 'reviews', 'colors', 'capacity']]
 
data.to_csv("product_list.csv")
```

### save as csv 

```
import csv
with open('product_test', 'w') as f:
    write = csv.writer(f)
    write.writerow(url)
    
```
