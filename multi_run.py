from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

import solScrape
import sys
from plogs import get_logger
import time

from multiprocessing import Pool

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

phrase = 'who'
key = "VERB"
start = None

def run(num):
    time.sleep(2)
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://corpus.byu.edu/coca/")
    time.sleep(2)
    
    fname='{}_{}_{}.log'.format(phrase, 'VERB', num)
    logging = get_logger()
    logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=False)

    try:
        solScrape.search(phrase, key, logging, driver, num_hits=1000)
        solScrape.findWord(phrase, key, num, logging, driver, start_at=start)
        driver.close()
    except Exception as e:
        logging.error(e)
        print("Exception: {}".format(e))

with Pool(10) as p:
    print(p.map(run, range(1, 1001)))
