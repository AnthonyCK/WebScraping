#pip install selenium
#download chromedriver.exe
#install chrome browser
#make sure that chrome and chromedriver have the same version level (e.g., 103)
#add chromedriver.exe to PATH

#maybe try to automatically get the chromedriver that mathes your chrome
#import chromedriver_autoinstaller
#chromedriver_autoinstaller.install()
#driver = webdriver.Chrome()


import os
from selenium import webdriver
import time

folder_path = ".\\advanced scraping\\"


#start the chromedriver
driver = webdriver.Edge(folder_path + "msedgedriver.exe")

#clout
#driver.get("https://yoururl.com")
driver.get("https://www.airbnb.com")

#give chrome some time to load the website
time.sleep(30)

#tell chrome to scroll down a bit
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#give chrome some time to load the website
time.sleep(30)

#tell chrome to scroll down a bit
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#give chrome some time to load the website
time.sleep(30)

#print(driver.page_source)

with open(folder_path + "output.html", "wb") as file:
    file.write(driver.page_source.encode("utf-8"))


file.close()
driver.close()

