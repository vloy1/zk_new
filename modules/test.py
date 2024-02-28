import random
import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="a")
try:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger('').addHandler(console_handler)
    logging.info(1)
    g = 0/0
except Exception as a:
    print(type(str(a)))
    logging.error(a)
