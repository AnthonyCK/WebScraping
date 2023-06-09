import pandas as pd
from bs4 import BeautifulSoup
import re
import os

import constants

def parse_data():
    list_for_writing = []

    # Iterate over files in folder_path
    for root, dirs, files in os.walk(constants.FOLDER_PATH):
        depth = root[len(constants.FOLDER_PATH):].count(os.sep)

        if depth == 1:  # Change this value to access directories at different depths
            for file in files:
                # Only iterate over .html files
                if file.endswith((".html")):
                    currentFile = os.path.join(root, file).replace('\\', '/')
                    # Open html file
                    with open(currentFile, encoding='utf8') as infile:
                        # Read the file into beautifulsoup
                        soup = BeautifulSoup(infile, "lxml")
                        
                        # Price, Name and Description 
                        temp_var = soup.find("div", {"class": "caption"}).findAll("h4")
                        name = temp_var[1].text
                        price = temp_var[0].text
                        description = soup.find('p', {'class': 'description'}).text

                        # Product rating (Number of stars)
                        temp_var = str(soup.find('div', {'class': 'ratings'}))
                        stars = temp_var.count('glyphicon-star')

                        # Number of reviews
                        temp_var = soup.find('div', {'class': 'ratings'}).text
                        reviews = int(re.findall(r'\b\d+\b', temp_var)[0])

                        # Colors (if available)
                        try:
                            dropdown = soup.find('div', {'class': 'dropdown'}).text
                            colors = ','.join(dropdown.split('\n')[3:-2])
                        except:
                            colors = ''

                        # Storage capacity (if available)
                        try:
                            temp_var = soup.findAll('button', {'type': 'button'})
                            capacity = ','.join([i.text for i in temp_var if len(re.findall('disabled', str(i))) == 0])
                        except:
                            capacity = ''

                        # Product categories and ID
                        temp_var = currentFile.split('/')
                        product_id = temp_var[-1].split('.')[0]
                        category_L1 = temp_var[-3]
                        category_L2 = temp_var[-2]

                        # Append to list
                        product = {'ID': product_id, 'L1': category_L1, 'L2': category_L2, "Product Name": name, "Price": price, 'Description': description, 'Stars': stars, 'Reviews': reviews, 'Colors': colors, 'Capacity': capacity}
                        list_for_writing.append(product)
    # Write to CSV
    data = pd.DataFrame(list_for_writing)
    data.to_csv(constants.OUTPUT_CSV, index=False)
