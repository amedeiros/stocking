(import atexit)
(import [slackbot.bot [Bot]])

(setv bot (Bot))
(setv bot._client.icon_emoji ":robot_face:")

(defn bot-msg [channel msg]
    (bot._client.send_message channel msg :as_user False))

(defn goodbye []
    (bot-msg "#general" "Shutting down..."))

(defmain [&rest args]
    (do
        (print "Starting!")
        (.register atexit goodbye)
        (bot-msg "#general" "Starting...")
        (.run bot)))