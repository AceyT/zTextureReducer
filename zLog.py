import logging as l
from logging.handlers import RotatingFileHandler

MAX_BYTES = 1024 * 1024 * 100 #MB
FILE_FORMATTER = l.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
STREAM_FORMATTER = l.Formatter('%(name)s :: %(levelname)s :: %(message)s')
LOG_LEVEL = l.ERROR

def create_logfile(filename:str):
	file_handler = RotatingFileHandler(filename, 'a', MAX_BYTES, 2)
	file_handler.setLevel(l.DEBUG)
	file_handler.setFormatter(FILE_FORMATTER)
	return file_handler

def create_logstream():
	stream_handler = l.StreamHandler()
	stream_handler.setLevel(LOG_LEVEL)
	stream_handler.setFormatter(STREAM_FORMATTER)
	return stream_handler

def setup_logger(logger_name:str):
	logger = None
	if logger_name:
		logger = l.getLogger(logger_name)
		logger.addHandler(create_logfile(logger_name + ".log"))
		logger.addHandler(create_logstream())
	else:
		logger = l.getLogger()
		logger.addHandler(create_logstream())
	logger.setLevel(LOG_LEVEL)
	return logger

LOGGER = None

def get_logger(name: str):
	global LOGGER
	if LOGGER == None:
		LOGGER = setup_logger(name)
	return LOGGER