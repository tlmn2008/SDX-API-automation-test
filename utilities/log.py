import logging
import sys


def setup_logger(name, logfile, level=logging.DEBUG):
    log_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d [%(funcName)s]: '
                                   '%(message)s', '%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # output to the screen, print log if log level is higher than DEBUG
    logstd = logging.StreamHandler()
    logstd.setLevel(logging.DEBUG)
    logstd.setFormatter(log_format)
    logger.addHandler(logstd)

    # output to the log file, write log to file if log level is higher than WARN
    logfile = logging.FileHandler(logfile, mode='w+')
    logfile.setFormatter(log_format)
    logfile.setLevel(logging.DEBUG)
    logger.addHandler(logfile)

    # Handle stderr, let stdout operate as normal, in order for print() to work
    class StreamToLogger(object):
        ''' Will just forward logs to the logger '''
        def __init__(self, logger, log_level):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            ''' Standard write function '''
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            ''' Standard flush function, nothing to do though '''
            pass
    sys.stderr = StreamToLogger(logger, logging.ERROR)

    return logger

