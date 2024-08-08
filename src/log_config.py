import logging


# creating a logger for capturing request & exception counts
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # set logger level to DEBUG to capture all the messages.

file_handler = logging.FileHandler(f'{__name__}.log', mode='a', encoding='utf-8')

formatter = logging.Formatter("{name} - {asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M",)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)