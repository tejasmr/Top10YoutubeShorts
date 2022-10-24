import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(ch)

fh = logging.FileHandler(r'latest_log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(fh)
