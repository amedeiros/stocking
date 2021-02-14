import os

from algo_bot import cache, utils
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

KEY = os.environ["ALPHA_VANTAGE_KEY"]
TIME_SERIES = TimeSeries(key=KEY, output_format="pandas", indexing_type="date")
SECTOR_PERFORMANCE = SectorPerformances(key=KEY, output_format="pandas")
TECH_INDICATORS = TechIndicators(key=KEY, output_format="pandas")
FUNDAMENTAL_DATA = FundamentalData(key=KEY, output_format="pandas")


def time_series_daily(symbol: str, outputsize="full"):
    key = f"time_series_daily:{symbol}:{utils.today()}"
    data = cache.read(key)
    if data is not None:
        return data

    data, _ = TIME_SERIES.get_daily(symbol=symbol, outputsize=outputsize)
    cache.write(key, data, cache.DEFAULT_TTL)
    return data


def time_series_intraday(symbol: str, interval="60min", outputsize="full"):
    data, _ = TIME_SERIES.get_intraday(
        symbol=symbol, outputsize=outputsize, interval=interval
    )
    return data


def sma(symbol: str, interval="daily", series_type="close", time_period="50"):
    key = f"sma:{symbol}:{time_period}:{utils.today()}"
    data = cache.read(key)
    if data is not None:
        return data

    data, _ = TECH_INDICATORS.get_sma(
        symbol=symbol,
        interval=interval,
        series_type=series_type,
        time_period=time_period,
    )

    cache.write(key, data, cache.DEFAULT_TTL)
    return data


def company_overview(symbol: str):
    key = f"company_overview:{symbol}"
    data = cache.read(key)
    if data is not None:
        return data

    data, _ = FUNDAMENTAL_DATA.get_company_overview(symbol=symbol)
    cache.write(key, data, cache.DEFAULT_TTL)
    return data


def sector_performance():
    data, _ = SECTOR_PERFORMANCE.get_sector()
    return data
