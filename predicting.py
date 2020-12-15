import pandas as pd
from fbprophet.forecaster import StanBackendEnum, Prophet as PR


class Prophet(PR):
    stan_backend: object

    def __init__(self, *args, **kwargs):
        self.stan_backend = None
        super().__init__(args, kwargs)


def prophet(data, field, daily_seasonality=True):
    p = Prophet(daily_seasonality=daily_seasonality, stan_backend=None)
    d = pd.DataFrame(data={"ds": data["dates"], "y": data[field]})
    p.fit(d)

    return p
