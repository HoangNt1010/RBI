from datetime import datetime
from dateutil.relativedelta import relativedelta

def dateFuture(date, yearAdd):
    return date + relativedelta(years=+ yearAdd)

def date2str(date):
    return date.strftime('%d/%m/%Y')
def dateFuturebyMonth(date, yearAdd,monthAdd, dayAdd):
    return date + relativedelta(years=+ yearAdd,months=+monthAdd, days=+dayAdd)
def date2strCC(date):
    return date.strftime('%m/%d/%Y')
def date2strCC2(date):
    return date.strftime('%Y/%m/%d')