import solScrape
import sys
from plogs import get_logger

phrase = sys.argv[1]
cont = sys.argv[2]
start = int(sys.argv[3])

if start == 0:
    start = None

fname='{}_{}_{}.log'.format(phrase, 'VERB', cont)

logging = get_logger()
logging.config(to_file=True, file_location='logs/', filename=fname, show_levels=True, show_time=True, pretty=True)

key = "VERB"
solScrape.search(phrase, key, logging, num_hits=1000)
solScrape.findWord(phrase, key, cont, logging, start_at=start)
solScrape.closeDriver()
