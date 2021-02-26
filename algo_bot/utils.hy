(import asyncio nest_asyncio)
(import json time os shlex)
(import boto3 plotly)
(import [dataclasses [dataclass]])
(import [datetime [datetime timedelta]])
(import [dateutil.relativedelta [relativedelta]])
(import [functools [wraps]])
(import [pandas :as pd])
(import [tabulate [tabulate]])
(import [algo_bot.slackbot_settings [BOT_ENV]])

(nest_asyncio.apply)

; Positioning Helpers

(with-decorator dataclass
    (defclass Positioning []
        (setv ^int position-size 0)
        (setv ^float max-loss-per-share 0.0)
        (setv ^float total-risk 0.0)
        (setv ^float total-gain 0.0)
        (setv ^float profit 0.0)
        (setv ^float purchase-cost 0.0)
        (setv ^float risk-reward-ratio 0.0)

        (defn to-df [self]
            (pd.DataFrame :data [(self.to_dict)]))

        (defn to-dict [self]
            {
                "position_size" self.position-size
                "max_loss_per_share" self.max_loss_per_share
                "total_risk" self.total_risk
                "total_gain" self.total_gain
                "profit" self.profit
                "purchase_cost" self.purchase_cost
                "risk_reward_ratio" self.risk_reward_ratio
            })))

(defn position-sizing-long [risk price stop exit]
    (setv max-loss-per-share (- price stop))
    (setv position-size (round-down (/ risk max-loss-per-share)))
    (setv max-gain (* position-size exit))
    (setv total-risk (* position-size max-loss-per-share))
    (setv cost (* position-size price))
    ; This line is the differece between short and long
    (setv profit (- max-gain cost))
    (setv risk-reward-ratio (/ (* (/ profit total-risk) 100) 100))
    (Positioning
        :position-size position-size
        :max-loss-per-share max-loss-per-share
        :total-risk total-risk
        :profit profit
        :purchase-cost cost
        :risk-reward-ratio risk-reward-ratio))

(defn position-sizing-short [risk price stop exit]
    (setv max-loss-per-share (- stop price))
    (setv position-size (round-down (/ risk max-loss-per-share)))
    (setv max-gain (* position-size exit))
    (setv total-risk (* position-size max-loss-per-share))
    (setv cost (* position-size price))
    ; This line is the differece between short and long
    (setv profit (- cost max-gain))
    (setv risk-reward-ratio (/ (* (/ profit total-risk) 100) 100))
    (Positioning
        :position-size position-size
        :max-loss-per-share max-loss-per-share
        :total-risk total-risk
        :profit profit
        :purchase-cost cost
        :risk-reward-ratio risk-reward-ratio))

; Message helpers
(defn attachments [message title title-link &optional [footer "Stocking Bot 0.1B"] [text None] [fields []]]
    [{
        "author_name" (get (get message.user "profile") "real_name")
        "title_link" title-link
        "title" title
        "color" f"#{(get message.user 'color)}"
        "text" text
        "footer" footer
        "fields" fields}])

(defn wrap-ticks [message]
    f"\n```\n{message}\n```")

(defn wrap-ticks-tabulate [df &optional [headers "keys"] [tablefmt "pipe"]]
    (wrap-ticks (tabulate df :headers headers :tablefmt tablefmt)))

(defn reply-webapi [message text]
    (message.reply-webapi text :as-user False))

(defn send-webapi [message text title &optional [title-link ""]]
    (message.send-webapi
        ""
        (json.dumps
            (attachments message :text text :title title :title-link title-link))
        :as-user False))

(defn processing [message]
    (reply-webapi message "Processing..."))

; Time and date helpers
(defn years-ago [&optional [years 1]]
    (.strftime
        (- (datetime.now) (relativedelta :years years))
        "%Y-%m-%d"))

(defn years-from-now [&optional [years 1]]
    (.strftime
        (+ (datetime.now) (relativedelta :years years))
        "%Y-%m-%d"))

(defn today []
    (.strftime
        (datetime.now)
        "%Y-%m-%d"))

; Helper to generate different signed urls
(defn url-builder [type]
    (fn [name &optional [bucket "stocks-am"]]
        (.generate-presigned-url (boto3.client "s3")
            :ClientMethod "get_object"
            :Params {
                "Bucket" bucket
                "Key" name
                "ResponseContentType" type})))

(setv html-url (url-builder "text/html"))
(setv image-url (url-builder "image/png"))

; Math helpers
(defn round-down [num &optional [divisor 10]]
    (- num (% num divisor)))

; Storage helpers
(defn store-s3 [filename name &optional [bucket "stocks-am"]]
    (setv s3 (boto3.resource "s3"))
    (.put (s3.Object bucket name) :Body (open filename "rb"))
    (os.remove filename))

(defn store-html [html name]
    (setv filename f"templates/{name}")
    (with [f (open filename "w")]
        (f.write "<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css\">\n")
        (f.write "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js\"></script>\n")
        (f.write "<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js\"></script>\n")
        (f.write html))
    (store-s3 filename name))

; Storage decorator for graphs
(defn graph-storage [func]
    (fn [fig name]
        (if (= BOT_ENV "development")
            (do
                (setv filename f"./templates/{name}")
                (func fig filename)
                (store-s3 filename name))
            (raise (RuntimeError f"Unknown environment {BOT_ENV}")))))

(with-decorator graph-storage
    (defn store-pyplat-graph [fig filename]
        (fig.savefig filename)))

(with-decorator graph-storage
    (defn store-graph [fig filename]
        (plotly.offline.plot fig :filename filename)))

; Begin Decorators

; Decorator to parse params from slack commands
(defn parse-params [parser &rest args]
    (fn [func]
        (fn [&rest args &kwargs kwargs]
            (setv params
                (parser.parse-args (shlex.split (get args 1))))
            (setv args (+ (,(get args 0) params) (cut args 2)))
            (func #*args #**kwargs))))

; Authentication decorator
(defn auth [func]
    ; Circular import otherwise
    (import [algo_bot.db.models [User]])
    (fn [&rest args &kwargs kwargs]
        (setv message (get args 0))
        (processing message)
        (setv user (.first (User.where :slack (get message.user "id"))))
        (if-not user
            (reply-webapi message "Error: must create an account!")
            (do
                (assoc message.user "db_user" user)
                (setv args (+ (, message) (cut args 1)))
                (func #*args #**kwargs)))))

; Decorator to create a new event loop and exit
(defn event-loop [func]
    (fn [&rest args &kwargs kwargs]
        (setv loop (asyncio.new_event_loop))
        (asyncio.set_event_loop loop)
        (setv result (func #*args #**kwargs))
        (loop.close)
        result))

; Decorator to wait for seconds and retry a function call
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
