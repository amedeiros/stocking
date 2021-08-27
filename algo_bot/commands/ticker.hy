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

(with-decorator (respond-to "^ticker (.*)" re.IGNORECASE)
    (defn ticker [message ticker]
        (setv df (alpha-vantage-client.company-overview ticker))
        (setv filename f"{ticker}_overview.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            :text (get (get df "Description") 0)
            :title "Overview for {ticker}"
            :title-link (utils.html-url filename))))


(with-decorator (respond-to "ticker-top5 (.*)" re.IGNORECASE)
    (defn ticker-top [message ticker]
        (setv df (.head (alpha-vantage-client.time-series-daily ticker)))
        (utils.reply-webapi message (utils.wrap-ticks-tabulate df))))
