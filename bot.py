from flask import Flask, request, Response
import telebot, os, json

api_token = API_TOKEN # Storing the token value of the bot
chat_id = CHAT_ID # The particular chat id to share the message alert
bot = telebot.TeleBot(api_token)

app = Flask(__name__)

@bot.message_handler(commands=['hello']) 
def hello_world(message):  # Basic hello world fuction to receive the chat_id
    bot.send_message(message.chat.id, "Hello, World! btw the chat_id is {}".format(message.chat.id))

@app.route('/' + api_token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]) # Decoding the incoming message from Telegram chat
    return Response("Cheers, love.", status=200)

@app.route("/", methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST': # If we receive a file from the page
        try:
            post_json = request.get_json() # Try to create a JSON object of POST
            text = post_json['plain'] # Getting the plain content of the e-mail message
            bot.send_message(chat_id, text)
            return Response("OK", status=200)
        except: pass # I'm lazy
    else:
        bot.remove_webhook() # Removing then setting the webhook is a good practice to avoid conflicts
        bot.set_webhook(url='HEROKUAPP_LINK' + api_token)
        return "<h1>Welcome to Price Watcher Bot</h1>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))