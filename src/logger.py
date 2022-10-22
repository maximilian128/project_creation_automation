# importing this file creates a Logger called logger, which can be used in the file which imports.

import logging
import inspect


# Formatter subclass that never prints tracebacks, even when logger.exception() is called.
class NoTracebackFormatter(logging.Formatter):
    def format(self, record):
        record.exc_text = "" # ensures formatException gets called
        return super(NoTracebackFormatter, self).format(record)

    def formatException(self, ei):
        return ""


# create Formatter instance for writing to log file (set the format of the logs)
f_format = logging.Formatter('%(levelname)s at %(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

# create Formatter instance for console output (set the format of the logs)
# class NoTracebackFormatter ensures that no tracebacks are printed to console even when logger.exception() is called.
c_format = NoTracebackFormatter('%(levelname)s - %(message)s')

# create file handler and set level and formatter
# only level ERROR and above gets written to log file
# f_handler = logging.FileHandler("logs.log", mode="w")
f_handler = logging.FileHandler("logs.log")
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(f_format)

# create console handler and set level and formatter
# only INFO and above gets printed to console
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(c_format)

# get filename of file which imports the logger.py file.
# this is the file where an error accured and which name gets printed as "name" into the logs.log file
if __name__ != '__main__':
    for frame in inspect.stack()[1:]:
            if frame.filename[0] != '<':
                fn = frame.filename.split("/")[-1]
                break
else:
    fn = __file__.split("/")[-1]

# create logger and add handler
logger = logging.getLogger(fn)
logger.setLevel(logging.DEBUG)
logger.addHandler(f_handler)
logger.addHandler(c_handler)


if __name__ == "__main__":

    class my_exept(Exception):
        pass

    def main():
        try:
            raise my_exept("Except text.")
        except my_exept as e:
            print("Hey:", e)
            logger.info("Here is an info.")
            raise



    try:
        main()
    except my_exept as e:
        logger.exception(e)
        print("Here 1", e)
        print("Here 2")