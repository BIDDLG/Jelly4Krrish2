import os
import time

class Config(object):
    NO_RESULTS_MSG = os.environ.get('NO_RESULTS_MSG', False)
    MOVIE_WEBSITE = os.environ.get('MOVIE_WEBSITE')
    # Get a bot token from botfather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")


    # Get from my.telegram.org
    API_ID = int(os.environ.get("API_ID", 12345))


    # Get from my.telegram.org
    API_HASH = os.environ.get("API_HASH", "")


    # Database URL from https://cloud.mongodb.com/
    DATABASE_URI = os.environ.get("DATABASE_URI", "")


    # Your database name from mongoDB
    DATABASE_NAME = str(os.environ.get("DATABASE_NAME", "Cluster0"))


    # ID of users that can use the bot commands
    AUTH_USERS = {str(x) for x in os.environ.get("AUTH_USERS", "").split()}


    # To save user details (Usefull for getting userinfo and total user counts)
    # May reduce filter capacity :(
    # Give yes or no
    SAVE_USER = os.environ.get("SAVE_USER", "no").lower()


    # Go to https://dashboard.heroku.com/account, scroll down and press Reveal API
    # To check dyno status
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")


    # OPTIONAL - To set alternate BOT COMMANDS
    ADD_FILTER_CMD = os.environ.get("ADD_FILTER_CMD", "add")
    DELETE_FILTER_CMD = os.environ.get("DELETE_FILTER_CMDD", "del")
    DELETE_ALL_CMD = os.environ.get("DELETE_ALL_CMDD", "delall")
    CONNECT_COMMAND = os.environ.get("CONNECT_COMMANDD", "connect")
    DISCONNECT_COMMAND = os.environ.get("DISCONNECT_COMMANDD", "disconnect")
    UPDATE_CHANNEL = int(os.environ.get("UPDATE_CHANNEL", "0"))


   # To record start time of bot
    BOT_START_TIME = time.time()
    REPLIT_USERNAME = os.environ.get("REPLIT_USERNAME", None) # your replit username 
    REPLIT_APP_NAME = os.environ.get("REPLIT_APP_NAME", None) # your replit app name 
    REPLIT = f"https://{REPLIT_APP_NAME.lower()}.{REPLIT_USERNAME}.repl.co" if bool(REPLIT_APP_NAME and REPLIT_USERNAME) else False
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", "300"))