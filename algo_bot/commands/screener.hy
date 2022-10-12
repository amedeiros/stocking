(import argparse)
(import [pandas :as pd])
(import [slackbot.bot [respond-to]])
(import [sqlalchemy.exc [IntegrityError]])
(import [algo-bot [utils]])
(import [algo-bot.db.models [Screener]])
(import [finviz.helper_functions.error_handling [NoResults]])

(setv SCREENER_PARSER (argparse.ArgumentParser))
(SCREENER_PARSER.add-argument "--name" :type str :required True)
(SCREENER_PARSER.add-argument "--filters" :type str :required True)
(SCREENER_PARSER.add-argument "--cron" :type str)

(with-decorator (respond-to "^screener-new (.*)")
                utils.auth
                (utils.parse-params :parser SCREENER_PARSER)
    (defn new-screener [message params]
        (setv user (get message.user "db_user"))
        (try
            (Screener.create 
                :name params.name
                :user user
                :filters params.filters
                :cron params.cron)
            (utils.reply-webapi message f"Succesfully created screener {params.name}.")
            (except [IntegrityError]
                (utils.reply-webapi message "Error: Screener already exists!")))))

(with-decorator (respond-to "^screener-list")
                utils.auth
    (defn screener-list [message]
        (setv user (get message.user "db_user"))
        (setv df (.set-index (pd.DataFrame :data (lfor x user.screeners (x.to-dict))) "id"))
        (utils.reply-webapi message (utils.wrap-ticks-tabulate df))))

(with-decorator (respond-to "^screener-run --id (.*)")
                utils.auth
    (defn screener-run [message id]
        (setv user (get message.user "db_user"))
        (setv screener (.first (Screener.where :id id :user_id user.id)))
        (if screener
            (do
                (try
                    (setv df (screener.run))
                    (setv filename (+ (screener.name.replace " " "_") "_screener.html"))
                    (utils.store-html (df.to-html :classes "table table-striped") filename)
                    (utils.send-webapi
                        message
                        ""
                        :title f"Screener Results: {screener.name}"
                        :title-link (utils.html-url filename))
                    (except [NoResults]
                        (utils.reply-webapi message f"No results for sceener: {screener.name}"))))
            ; Else report missing screener
            (utils.reply-webapi message f"Error: No Screener with ID {id}"))))        
