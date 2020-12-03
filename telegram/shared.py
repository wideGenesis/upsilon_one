import datetime
import sys

ORDER_MAP = {}


def datetime2int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))


def int2datetime(dt_int):
    return datetime.strptime(str(dt_int), "%Y%m%d%H%M%S")


class PrintLogger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
