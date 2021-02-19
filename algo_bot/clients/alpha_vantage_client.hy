(import os time)
(import [algo_bot.cache [cache-memoize]] )
(import [typing [Tuple]])
(import [alpha_vantage.fundamentaldata [FundamentalData]])
(import [alpha_vantage.sectorperformance [SectorPerformances]])
(import [alpha_vantage.techindicators [TechIndicators]])
(import [alpha_vantage.timeseries [TimeSeries]])

(setv KEY
    (os.environ.get "ALPHA_VANTAGE_KEY"))
(setv TIME_SERIES
    (TimeSeries :key KEY :output_format "pandas" :indexing_type "data"))
(setv SECTOR_PERFORMANCE
    (SectorPerformances :key KEY :output_format "pandas"))
(setv TECH_INDICATORS
    (TechIndicators :key KEY :output_format "pandas"))
(setv FUNDAMENTAL_DATA
    (FundamentalData :key KEY :output_format "pandas"))

; Decorator to wait for seconds and retry a function call
; TODO: Move to utils when ported to Hy.
(defn with-backoff [exception &optional [wait-seconds 60]]
    (fn [func]
        (fn [&rest args &kwargs kwargs]
            (while True
                (try
                    (setv results (func #*args #**kwargs))
                    (break)
                    (except [exception]
                        (print "Backing off...")
                        (time.sleep wait-seconds))))
            results)))

(with-decorator (cache-memoize "time-series-daily")
                (with-backoff ValueError)
    (defn time-series-daily [symbol &optional [outputsize "full"]]
        (first (TIME_SERIES.get_daily :symbol symbol :outputsize outputsize))))

(defn time-series-intraday [symbol &optional [interval "60min"] [outputsize "full"]]
    (first (TIME_SERIES.get_intraday :symbol symbol :outputsize outputsize :interval interval)))

(with-decorator (cache-memoize "sma")
                (with-backoff ValueError)
    (defn sma [symbol &optional [interval "daily"] [series-type "close"] [time-period "50"]]
        (first
            (TECH_INDICATORS.get_sma :symbol symbol :interval interval :series_type series-type :time_period time-period))))

(with-decorator (cache-memoize "company-overview")
    (defn company-overview [symbol]
        (first
            (FUNDAMENTAL_DATA.get_company_overview :symbol symbol))))

(with-decorator (cache-memoize "sector-performance")
    (defn sector-performance []
        (first
            (SECTOR_PERFORMANCE.get_sector))))
