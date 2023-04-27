
#pip install bs4
#pip install lxml

import re
import csv
from bs4 import BeautifulSoup
import os


folder_path = "/Users/jfoerderer/LRZ Sync+Share/Web Scraping for Scientists (SS2023) (Jens Förderer) (Johannes Gölz)/sample code/parse/html dump/"

#prepare output dataset
output_filename = "products.csv"
output_path = os.path.join(folder_path, output_filename)
dataset = open(output_path, 'w', newline='', encoding="utf-8")
wr = csv.writer(dataset, quoting=csv.QUOTE_ALL)

#write header row to output
list_for_writing = []
list_for_writing.extend(["name", "price"])
wr.writerow(list_for_writing)
dataset.flush()
os.fsync(dataset)
list_for_writing = []

#iterate over files in folder_path
for root, dirs, files in os.walk(folder_path):
    for file in files:
        #only iterate over .html files
        if file.endswith((".html")):
            currentFile = os.path.join(root, file)
            #open html file
            with open(currentFile, encoding='utf8') as infile:
                
                #read the file into beautifulsoup
                soup = BeautifulSoup(infile, "lxml")

                #extract data
                #print(soup)
                data = soup.find("div", {"class" : "caption"}).findAll("h4")
                name = data[1].text
                price = data[0].text
                
                list_for_writing.extend([name, price])
                
                wr.writerow(list_for_writing)
                list_for_writing=[]
dataset.flush()
os.fsync(dataset)
dataset.close()