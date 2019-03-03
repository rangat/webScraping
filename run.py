import solScrape
import sys
from plogs import get_logger

p = sys.argv[1]
cont = sys.argv[2]
start = sys.argv[3]

if start == '0':
    start = None
else:
    start = int(start)

fname='{}_{}_{}.log'.format(p, 'VERB', cont)

logging = get_logger()
logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=True)

phrase = p
key = "VERB"
solScrape.search(phrase, key, logging)
solScrape.findWord(phrase, key, cont, logging, start_at=start)
solScrape.closeDriver()
