(import re)
(import [slackbot.bot [respond-to]])
(import [algo-bot [utils]])
(import [algo-bot.slackbot-settings [BOT_ENV]])

(defn _respond [message response]
 (utils.reply-webapi message (utils.wrap-ticks response)))

(with-decorator (respond-to "^help" re.IGNORECASE)
    (defn help [message]
        (_respond message
f"
Stocking bot help sub-commands ({BOT_ENV})

    @stockbot manual-help (Display manual analysis commands)
    @stockbot user-help (Display user commands)
    @stockbot screener-help (Display screener commands requires user account)
    @stockbot strategies-help (Display help for strategies)
    @stockbot watchlist-help (Display help for watchlists)
")))

(with-decorator (respond-to "strategies-help" re.IGNORECASE)
    (defn strategies-help [message]
        (_respond message
f"
Stocking bot strategy commands requires an account ({BOT_ENV})

    @stockbot strategy-risk-vs-reward --screener-id ID (Run the strategy with the specified stock screener.)
    @stockbot strategy-turtle --screener-id ID (Run the turtle trader straategy for this screener.)
")))

(with-decorator (respond-to "^screener-help" re.IGNORECASE)
    (defn screener-help [message]
        (_respond message
f"
Stocking bot screener commands requires an account ({BOT_ENV})

    @stockbot screener-new --name NAME --filters FILTERS (csv string) --cron CRON (Optional)
    @stockbot screener-list (Display your screeners)
    @stockbot screener-run --id ID (Run a screener you own)
")))


(with-decorator (respond-to "^user-help" re.IGNORECASE)
    (defn user-help [message]
        (_respond message
f"
Stocking bot user commands ({BOT_ENV})

    @stockbot user-new --email EMAIL --first_name FIRST_NAME --last_name LAST_NAME
")))


(with-decorator (respond-to "^manual-help" re.IGNORECASE)
    (defn manual-help [message]
        (_respond message
f"
Stocking bot help manual analysis ({BOT_ENV})

    @stockbot ticker TICKER (AlphaVantage Overview)
    @stockbot news TICKER (Returns news from FinViz as individual messages of URL's to unfurl)
    @stockbot news-compact TICKER (Returns news from FinViz as one message results in no unfurling)
    @stockbot interest-over-time TICKER (Chart news interest over time)
    @stockbot ticker-top5 TICKER (Returns last five days of open, close, high, low and volume)
    @stockbot candlestick TICKER (Link to a candlestick chart for the supplied ticker)
    @stockbot screener FILTERS (Finviz screener comma seperated filters EX: @stockbot screener exch_nasd,geo_usa,sh_price_u5,ta_sma50_cross200a)
    @stockbot ticker-performance TICKER (Finviz performance table)
    @stockbot ticker-overview TICKER (Finviz overview table)
    @stockbot ticker-technical TICKER (Finviz technical table)
    @stockbot ticker-ownership TICKER (Finviz ownership table)
    @stockbot ticker-financial TICKER (Finviz financial table)
    @stockbot insider TICKER (List last 10 insider trades)
    @stockbot sector-performance (Get back sector performance)
    @stockbot sma TICKER (Chart of the simple moving average)
    @stockbot golden-cross TICKER (50SMA cross over the 200SMA)
")))

(with-decorator (respond-to "^watchlist-help" re.IGNORECASE)
    (defn watchlist-help [message]
        (_respond message
f"
Stocking bot watchlist commands ({BOT_ENV})

    @stockbot watchlist-new --name NAME --ticker TICKER (Create a new watchlist and add a ticker)
    @stockbot watchlist-list (List all of your watchlists)
    @stockbot watchlist-add-ticker --id WATCHLIST_ID --ticker TICKER (Add a ticker to an existing watchlist)
    @stockbot watchlist-del-ticker --id WATCHLIST_ID --ticker TICKER (Remove a ticker from an existing watchlist)
    @stockbot watchlist-view --id WATCHLIST_ID (Latest open, close etc of the tickers in an existing watchlist)
")))
