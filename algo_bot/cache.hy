(import [algo_bot.settings [AlgoBotSettings get_settings]])
(import [algo_bot [utils]])
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

; Decorator
(defn cache-memoize [key]
    (fn [func]
        (fn [&rest args &kwargs kwargs]
            ; TODO: Improve this cahce key it sucks make a hashing funciton
            (setv cache-key f"{key}:{args}:{kwargs}:{(utils.today)}")
            (setv data (read cache-key))
            ; Weird None check for dataframe not a problem in python with `data is not None` shurg.
            (if (= (type data) (type None))
                (do
                    (setv data (func #*args #**kwargs))
                    (write :key cache-key :value data)))
            data)))
