(import [pytrends.request [TrendReq]])

(defn interest-over-time [kw-list]
    (do
        (setv pytrend (TrendReq :hl "en-US"))
        (pytrend.build_payload :kw_list kw-list :gprop "news")
        (pytrend.interest_over_time)))

(defn suggestions [arg]
    (do
        (setv pytrend (TrendReq :hl "en-US"))
        (pytrend.suggestions arg)))
