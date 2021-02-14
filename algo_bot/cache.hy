(import [algo_bot.settings [AlgoBotSettings get_settings]])
(import redis)
(import pickle)

(setv settings (get_settings))
(setv REDIS_CLIENT (redis.Redis :host settings.redis-host :port settings.redis-port :db 0))
(setv DEFAULT_TTL (* 60 60)) ; One hour

(defn write [key value &optional [expire-at DEFAULT_TTL]]
    (REDIS_CLIENT.setex key expire-at (.dumps pickle value)))

(defn read [key]
    (if (REDIS_CLIENT.exists key) (pickle.loads (REDIS_CLIENT.get key))
        None))
