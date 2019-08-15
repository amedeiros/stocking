from fbprophet import Prophet
import pandas as pd


def prophet(data, field, daily_seasonality=True):
    p = Prophet(daily_seasonality=daily_seasonality)
    d = pd.DataFrame(data={'ds': data['dates'], 'y': data[field]})
    p.fit(d)

    return p
