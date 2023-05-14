import logging

__all__ = ['create_logger']


def create_logger(logger_file=None, logger_name='BabelTower',
                  logger_level=logging.INFO):
    r"""Configures and returns a logger.

    Args:
        logger_file: The path to the log file, defaults to None (no log file).
        logger_name: The name of the logger.
        logger_level: The log level for the logger, defaults to INFO.

    Return:
        A configured logger.
    """

    # Create a logger.
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    # Create a formatter for the log messages.
    formatter = logging.Formatter('%(asctime)s - '
                                  '%(name)s - '
                                  '%(levelname)-8s - '
                                  '%(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if logger_file:
        file_handler = logging.FileHandler(logger_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    _logger = create_logger('my_log_file.log', logger_level=logging.DEBUG)
    _logger.debug('debug message')
    _logger.info('info message')
    _logger.warning('warning message')
    _logger.error('error message')
    _logger.critical('critical message')
