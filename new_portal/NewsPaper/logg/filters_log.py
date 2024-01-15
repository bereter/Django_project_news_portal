import logging


class ContextFilter(logging.Filter):

    def filter(self, record):
        if record.levelname == 'DEBUG' or record.levelname == 'INFO':
            record.pathname = ''
            record.exc_info = ''
        elif record.levelname == 'WARNING':
            record.exc_info = ''
        return True
