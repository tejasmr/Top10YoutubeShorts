import logging
import os

LOG_FILE = r'latest_log.txt'

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(ch)

fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(fh)
