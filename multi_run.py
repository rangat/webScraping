import solScrape
import sys
from plogs import get_logger
import time
from multiprocessing import Pool

phrase = 'who'
key = "VERB"
start = None

def run(num):
    time.sleep(2)
    
    fname='{}_{}_{}.log'.format(phrase, 'VERB', num)
    logging = get_logger()
    logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=False)

    try:
        solScrape.search(phrase, key, logging, num_hits=1000)
        solScrape.findWord(phrase, key, num, logging, start_at=start)
        solScrape.closeDriver()
    except Exception as e:
        logging.error(e)
        print("Exception: {}".format(e))

with Pool(4) as p:
    print(p.map(run, range(1, 1001)))
