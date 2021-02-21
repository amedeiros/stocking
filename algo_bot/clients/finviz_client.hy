(import asyncio nest_asyncio finviz)
(import [algo-bot.utils [event-loop]])
(import [pandas :as pd])
(import [finviz.screener [Screener]])


(with-decorator event-loop
    (defn screener [&optional [filters ["exch_nasd" "sh_avgvol_o200" "sh_price_u5" "ta_change_u10" "geo_usa"]] [order "-volume"]]
        (setv stock-list (Screener :filters filters :order order))
        (setv df (pd.DataFrame stock-list.data))
        (df.set_index "Ticker" :drop False)
        df))

; Finviz table function generator
(defn finviz-table [table]
    (with-decorator event-loop
        (fn [ticker]
            (setv s (Screener :table table :tickers [ticker]))
            (pd.DataFrame s.data))))

(setv finviz-performance (finviz-table "Performance"))
(setv finviz-overview (finviz-table "Overview"))
(setv finviz-technical (finviz-table "Technical"))
(setv finviz-ownership (finviz-table "Ownership"))

(defn finviz-get-insider [stock]
    (finviz.get_insider stock))

(defn finviz-get-news [stock]
    (setv news (finviz.get_news stock))
    (setv table (pd.DataFrame news))
    (setv table.columns ["Title" "Link"])
    table)
