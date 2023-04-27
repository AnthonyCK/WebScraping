#pip install requests
from urllib.request import Request, urlopen
import csv
import os

#folder
folder_path = "./"

#sample frame
frame = "frame.csv"
fullinput = os.path.join(folder_path, frame)

def fetchData():
    #read frame
    with open(fullinput, encoding='utf8') as f:
        r = csv.reader(f, delimiter=',')
        
        #iterate over the lines in the frame (i.e., each URL)
        for row in r:

            url = row[0]
            #print(url)            
            req = Request(url)
            response = urlopen(req)

            #prepare file name
            file_name = url.split("/")[-1]

            with open(folder_path + str(file_name), 'wb') as file:
                file.write(response.read())           
            
if __name__ == '__main__':
    fetchData()