from datetime import datetime, timedelta
from math import log
import logging
import configs

epoch = datetime(1970, 1, 1)

def epoch_second(date):
    if not isinstance(date, datetime):
        date = datetime.fromtimestamp(date)
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs * 2

def hot(ups, downs, date):  
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0.1
    seconds = epoch_second(date) - 1134028003
    r = round(order + sign * seconds / 45000, 7)
    return r

def hot2(ups, downs, views, comments, quality, date):
    up_down_score = hot(ups, downs, date)
    return up_down_score * log(views + 2) * log(comments + 2)