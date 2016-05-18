# Initate logging loggers, and handlers
import logging


# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)


# create formatter
DEFAULT_FORMAT = '[%(levelname)s]: [%(asctime)s]  [%(name)s] [%(module)s:%(lineno)d] - %(message)s'
DEFAULT_DATE_FORMAT = '%d-%m-%y %H:%M:%S'
formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)

# add formatter to handler
handler.setFormatter(formatter)

# initiate a logger
logger = logging.getLogger(__name__)

# set level for Logger
logger.setLevel(logging.INFO)

# add handler to logger
logger.addHandler(handler)
