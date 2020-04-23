# Before executing the script, we need urllib3. Run `pip install urllib3`
import shutil
import zipfile
import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from git import Repo
import time

def download_covid_zip_files(path):
    url = "https://covid-19.bsvgateway.org/"
    options = webdriver.ChromeOptions() 
    prefs = {'download.default_directory' : path}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe",chrome_options=options)
    driver.get(url)
    triggerPush = False
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "us-model-outputs-links")))
        rows = element.find_elements(By.TAG_NAME, "tr")
        # Get the columns (all the column 2)        
        cols = rows[1].find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
        for col in cols:
            ele = col.find_elements(By.TAG_NAME, "a")[0]
            name = ele.get_attribute('href').split('/')[-1]
            filepath = path + '\\' + name
            if os.path.exists(filepath):
                continue
            else:
                triggerPush = True
                driver.get(ele.get_attribute('href'))
                time.sleep(3)
    finally:
        driver.quit()
    
    if triggerPush:
        repo = Repo(path)
        repo.git.add(path+'\\*')
        repo.git.commit( m='Add new Lanl raw data' )
        repo.git.pull()
        repo.git.push()

if __name__ == '__main__':
    path = sys.argv[1]
    download_covid_zip_files(path)
   