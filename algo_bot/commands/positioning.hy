(import argparse re)
(import [slackbot.bot [respond-to]])
(import [algo-bot [utils]])

(setv POSITION_PARSER (argparse.ArgumentParser))
(POSITION_PARSER.add-argument "--risk" :type float :required True)
(POSITION_PARSER.add-argument "--price" :type float :required True)
(POSITION_PARSER.add-argument "--exit" :type float :required True)
(POSITION_PARSER.add-argument "--stop" :type float :required True)

(with-decorator (respond-to "^positioning-long (.*)" re.IGNORECASE)
                (utils.parse-params :parser POSITION_PARSER)
    (defn position-long [message params]
        (setv r (utils.position-sizing-long params.risk params.price params.stop params.exit))
        (utils.reply-webapi message (utils.wrap-ticks-tabulate (r.to-df)))))
