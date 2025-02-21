import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Bot

app = Flask(__name__)
CORS(app)

TOKEN = ''
CHAT_ID = ''


def sendBot(name, content, confirm):
    bot = Bot(TOKEN)
    text = "Name: " + name + "\n" + "Sent you a wish: " + content + "\n" + confirm
    try:
        bot.sendMessage(
            CHAT_ID,
            text
        )
    except:
        print("Looks like CHAT_ID or TOKEN of telegram-bot was wrong!")


@app.route('/wishes', methods=['POST'])
def wishes():
    turnstile_token = request.form.get("cf-turnstile-response")
    secret_key = ""
    # print(turnstile_token)

    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": secret_key, "response": turnstile_token},
        )
        response_data = response.json()
        print(response_data.get("success"))
        if response_data.get("success"):
            data = request.form.to_dict()
            name = request.form.get('name')
            content = request.form.get('content')
            if "confirm" not in data:
                attend = "Chưa xác nhận tham dự"
            elif request.form.get('content') == "nha-trai":
                attend = "Xác nhận tham dự tại nhà trai"
            else:
                attend = "Xác nhận tham dự tại nhà gái"
            sendBot(name, content, attend)

            return jsonify({"message": "Data sent successfully"})
        else:
            return jsonify({"message": "Turnstile verification failed"}), 400
    except Exception as e:
        return jsonify({"message": "Error verifying Turnstile token"}), 500


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080")
