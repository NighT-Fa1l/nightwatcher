from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run).start()
    
    # Your Discord bot code below
    import discord
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    client.run(os.getenv('DISCORD_TOKEN'))
