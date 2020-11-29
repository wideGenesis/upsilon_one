import datetime

ORDER_MAP = {}


def datetime2int(dt):
    return int(dt.strftime("%Y%m%d%H%M%S"))


def int2datetime(dt_int):
    return datetime.strptime(str(dt_int), "%Y%m%d%H%M%S")
