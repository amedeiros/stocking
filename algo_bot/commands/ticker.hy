(import re)
(import [slackbot.bot [respond-to]])
(import [algo-bot [charting utils]])
(import [algo-bot.clients [alpha-vantage-client]])


(with-decorator (respond-to "candlestick (.*)" re.IGNORECASE)
    (defn candlestick [message ticker &optional [interval "60min"]]
        (utils.processing message)
        (setv time-series (alpha-vantage-client.time_series_intraday ticker :interval interval))
        (setv fig (charting.candlestick-plot time-series))
        (setv filename f"{ticker}_candlestick.html")
        (utils.store-graph fig filename)
        (utils.send-webapi
            message
            ""
            :title f"Candlestick Chart For {ticker}"
            :title-link (utils.html-url filename))))

; (with-decorator (respond-to "^ticker (.*)" re.IGNORECASE)
;     (defn ticker [message ticker]
;         (setv df )))
