import logging

logging.basicConfig(
        filename='events.log',
        format='%(levelname)s: %(message)s - %(asctime)s',
        level=logging.DEBUG
)


def info(message):
    logging.info(message)
    msg = open('events.log', 'r').readlines()
    print(msg[-1].strip())


def warning(message):
    logging.warning(message)
    msg = open('events.log', 'r').readlines()
    print(msg[-1].strip())


def critical(message):
    logging.critical(message)
    msg = open('events.log', 'r').readlines()
    print(msg[-1].strip())