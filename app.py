from flask import Flask, request, Response, jsonify
import requests
import json

app = Flask(__name__)

VALID_KEYS = ["eris77", "swrovh336"]
EXTERNAL_API = "https://hideme.eu.org/lookup?api=aadhar-info&key=eris001&aadhar={}"


@app.route("/aadhar", methods=["GET"])
def aadhar():
    key = request.args.get("key")
    aadhar = request.args.get("aadhar")

    # 🔐 API KEY
    if key not in VALID_KEYS:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "Invalid API Key",
            "DEVELOPER": "@iameris"
        })

    # 📱 VALIDATION
    if not aadhar or not aadhar.isdigit() or len(aadhar) != 12:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "Invalid Aadhar number. Please provide a valid 12-digit Aadhar number.",
            "DEVELOPER": "@iameris"
        })

    try:
        url = EXTERNAL_API.format(aadhar)
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return jsonify({
                "SUCCESS": False,
                "MESSAGE": "API Error",
                "DEVELOPER": "@iameris"
            })

        # 🔥 RAW JSON LOAD
        try:
            data = json.loads(res.text)
        except:
            return jsonify({
                "SUCCESS": False,
                "MESSAGE": "Invalid API Response",
                "DEVELOPER": "@iameris"
            })

        # ✅ ONLY CHANGE USERNAME (बाकी सब same)
        if "DEVELOPER" in data:
            data["DEVELOPER"] = "@iameris"

        if "BUY" in data:
            data["BUY"] = "💎 Premium API Access Available — DM @iameris on Telegram to Get Started!"

        # 🔥 RETURN SAME STRUCTURE
        return Response(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json"
        )

    except Exception:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "API Error",
            "DEVELOPER": "@iameris"
        })


if __name__ == "__main__":
    app.run(debug=True)
