import datetime
from dateutil.relativedelta import relativedelta

def date_today():
    date_today = (datetime.date.today())
    return date_today

def offer_date(offer_window_day, offer_window_time):
    now = datetime.datetime.now()
    time_now = (now+relativedelta(minutes=offer_window_time-100)).strftime("%H:%M:%S")
    date_offset_offer = datetime.date.today() + relativedelta(days=offer_window_day)
    offer_date_time = str(date_offset_offer) + 'T' + str(time_now) + 'Z'
    return offer_date_time