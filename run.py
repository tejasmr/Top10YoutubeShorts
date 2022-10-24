from logging import info, debug, warning, error, critical, basicConfig, DEBUG

basicConfig(level=DEBUG, format='[%(levelname)s] %(message)s')

if __name__ == "__main__":
    info('Ran the program successfully')