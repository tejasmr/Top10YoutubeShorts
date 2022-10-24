import sys

DEBUG = True

def log(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    if DEBUG:
        print(*objects, sep=sep, end=end, file=file, flush=flush)