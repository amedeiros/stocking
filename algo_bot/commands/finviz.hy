(import re)
(import [pandas :as pd])
(import [slackbot.bot [respond-to]])
(import [algo-bot [utils]])
(import [algo-bot.clients [finviz-client]])

(with-decorator (respond-to "^screener (.*)" re.IGNORECASE)
    (defn screener [message filters]
        (utils.processing message)
        (setv df (finviz-client.screener :filters (filters.split ",")))
        (setv filename (+ (filters.replace "," "_") "screener.html"))
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title "FinViz Screener Results"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-performance (.*)")
    (defn ticker-performance [message ticker]
        (utils.processing message)
        (setv df (finviz-client.finviz-performance :ticker ticker))
        (setv filename f"{ticker}_performance.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"Performance for {ticker}"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-overview (.*)")
    (defn ticker-overview [message ticker]
        (utils.processing message)
        (setv df (finviz-client.finviz-overview :ticker ticker))
        (setv filename f"{ticker}_overview.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"Overview for {ticker}"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-technical (.*)")
    (defn ticker-technical [message ticker]
        (utils.processing message)
        (setv df (finviz-client.finviz-technical :ticker ticker))
        (setv filename f"{ticker}_technical.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"Technical for {ticker}"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-ownership (.*)")
    (defn ticker-ownership [message ticker]
        (utils.processing message)
        (setv df (finviz-client.finviz-ownership :ticker ticker))
        (setv filename f"{ticker}_ownership.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"Ownership for {ticker}"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-financial (.*)")
    (defn ticker-financial [message ticker]
        (utils.processing message)
        (setv df (finviz-client.finviz-financial :ticker ticker))
        (setv filename f"{ticker}_financial.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"Financials for {ticker}"
            :title-link (utils.html-url filename))))

(with-decorator (respond-to "ticker-insider (.*)")
    (defn ticker-insider [message ticker]
        (utils.processing message)
        (setv df (pd.DataFrame (finviz-client.finviz-get-insider ticker)))
        (setv filename f"{ticker}_insider.html")
        (utils.store-html (df.to-html :classes "table table-striped") filename)
        (utils.send-webapi
            message
            ""
            :title f"insider for {ticker}"
            :title-link (utils.html-url filename))))
