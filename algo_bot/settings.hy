(import os)
(import [dataclasses [dataclass]])

(setv env (.get os.environ "BOT_ENV" "development"))

#@(dataclass (defclass AlgoBotSettings []
    (setv ^str redis-host None)
    (setv ^int redis-port None)
    (setv ^str db-host None)
    (setv ^str db-name None)
    (setv ^str db-password None)
    (setv ^str db-username None)
    (setv ^str bot-env None)))

(defn _dev_settings []
    (AlgoBotSettings
        :redis-host "redis"
        :redis-port 6379
        :db-host "db"
        :db-name "algo-bot"
        :db-password "root"
        :db-username "root"
        :bot-env "development"))

(defn _test_settings [] (_dev_settings))

(defn get-settings []
    (if (= env "development") (_dev_settings)
        (= env "testing") (_test_settings)))
