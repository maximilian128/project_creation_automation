import logging


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
c_format = NoTracebackFormatter('%(levelname)s at %(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S')

# create file handler and set level and formatter
# only level WARNING and above gets written to log file
f_handler = logging.FileHandler("logs.log", mode="w")
f_handler.setLevel(logging.WARNING)
f_handler.setFormatter(f_format)

# create console handler and set level and formatter
# only INFO and above gets printed to console
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(c_format)

# create logger and add handler
logger = logging.getLogger(__name__)
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
            raise



    try:
        main()
    except my_exept as e:
        logger.exception(e)
        print("Here 1", e)
        print("Here 2")