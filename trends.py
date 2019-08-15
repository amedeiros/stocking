from pytrends.request import TrendReq


def interest_over_time(kw_list):
    pytrend = TrendReq(hl='en-US')
    pytrend.build_payload(kw_list=kw_list, gprop='news')
    return pytrend.interest_over_time()


def suggestions(arg):
    pytrend = TrendReq(hl='en-US')
    return pytrend.suggestions(arg)
