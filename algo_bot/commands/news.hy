(import re)
(import [pandas :as pd])
(import [slackbot.bot [respond-to]])
(import [algo-bot [charting utils]])
(import [algo-bot.clients [finviz-client trends]])

(with-decorator (respond-to "^news (.*)" re.IGNORECASE)
    (defn news [message ticker]
        (for [url (get-news-urls ticker)]
            (utils.reply-webapi message f"\n{url}"))))


(with-decorator (respond-to "^interest-over-time (.*)" re.IGNORECASE)
    (defn interest-over-time [message ticker]
        (utils.processing message)
        (setv interest (trends.interest-over-time ticker))
        (setv df (pd.DataFrame interest))
        (setv fig (charting.line-chart-trends df))
        (setv filename f"{ticker}_interest_over_time.html")
        (utils.store-graph fig filename)
        (utils.send-webapi message
                            ""
                            :title f"Interest Over Time: {ticker}"
                            :title-link (utils.html-url filename))))

(defn get-news-urls [ticker]
    (setv urls [])
    (setv table (finviz-client.finviz-get-news ticker))
    (for [(, _ url) (.iterrows (table.head))]
        (urls.append (url.get "Link")))
    urls)
