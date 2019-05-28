from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import pprint as p
import json

import solScrape
import sys
from plogs import get_logger
import time

from multiprocessing import Pool

import os

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

phrase = 'who'
key = "VERB"
start = None

def init_driver():
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://corpus.byu.edu/coca/")
    time.sleep(2)
    return driver

def run(context):
    driver = init_driver()
    
    fname='{}_{}_{}.log'.format(phrase, 'VERB', context)
    logging = get_logger()
    logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=False)

    try:
        solScrape.search(phrase, key, logging, driver, num_hits=1000)
        solScrape.findWord(phrase, key, context, logging, driver, start_at=start)
        solScrape.save_htmls(phrase, key, context, logging, driver)
        driver.close()
    except Exception as e:
        logging.error(str(e))
        driver.close()

def pool_handler(phrases:tuple):
    p = Pool(10)
    p.map(run, phrases)

def get_freqencies(phrase):
    fname='{}_frequencies.log'.format(phrase)
    logging = get_logger()
    logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=False)

    solScrape.search(phrase, key, logging ,driver, num_hits=1000)

    frame = driver.find_element_by_name('x2')
    driver.switch_to_frame(frame)

    if not os.path.exists('{}/'.format(phrase)):
        os.mkdir(phrase)
   
    with open('{}/frequencies.html'.format(phrase), 'w') as w:
        w.write(driver.page_source)
    
    driver.close()

def generate_frequencies_dict(phrase):
    ret = {}
    file = '{}/frequencies.html'.format(phrase)
    
    if not os.path.isfile(file):
        print("File DNE")
    
    soup = None

    with open (file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    rows = soup.find_all("tr")[2:-2]
    for row in rows:
        row_data = row.find_all('td')

        context = row_data[2].get_text().strip()
        quantity = int(row_data[3].get_text().strip())
        ret[context] = quantity
    
    with open ('{}/frequencies.json'.format(phrase), 'w') as j:
        json.dump(ret, j)
    
    return ret



# init_driver()
# get_freqencies(phrase)
# generate_frequencies_dict(phrase)