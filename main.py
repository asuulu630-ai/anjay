from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.get("/webhook")
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


@app.post("/webhook")
def receive_message():
    data = request.get_json(silent=True) or {}

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        sender = message["from"]
        text = message.get("text", {}).get("body", "").lower().strip()

        if text == "menu":
            reply = (
                "🤖 MENU BOT\n\n"
                "1. Harga\n"
                "2. Promo\n"
                "3. Link Web\n\n"
                "Ketik salah satu menu."
            )

        elif text == "harga":
            reply = "💰 Silakan cek harga terbaru di website kami."

        elif text == "promo":
            reply = "🔥 Cek promo terbaru di website kami."

        elif text == "link":
            reply = "🌐 Website: https://contoh.com"

        else:
            reply = "Ketik *menu* untuk melihat daftar perintah."

        send_message(sender, reply)

    except (KeyError, IndexError, TypeError):
        pass

    return jsonify({"status": "ok"}), 200


def send_message(to, message):
    url = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    requests.post(url, headers=headers, json=payload, timeout=15)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))