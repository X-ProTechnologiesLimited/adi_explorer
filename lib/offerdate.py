# Filename: lib/offerdate.py
"""
Created on June 01, 2020
@author: Krishnendu Banerjee
@summary: This function helps in calculating the offer date and time
"""
import datetime
from dateutil.relativedelta import relativedelta

def date_today():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Return todays timestamp
    :access: public.
    :return: todays timestamp
    """
    date_today = (datetime.date.today())
    return date_today

def offer_date(offer_window_day, offer_window_time):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Calculate the Offer Date Time as per the Time delta specified
    :access: public.
    :param offer_window_day: Offset number of days
    :param offer_window_time: Offset number of minutes
    :return:
    """
    now = datetime.datetime.now()
    time_now = (now+relativedelta(minutes=offer_window_time-100)).strftime("%H:%M:%S")
    date_offset_offer = datetime.date.today() + relativedelta(days=offer_window_day)
    offer_date_time = str(date_offset_offer) + 'T' + str(time_now) + 'Z'
    return offer_date_time