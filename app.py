from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VALID_KEYS = ["eris77", "swrovh336"]

EXTERNAL_API = "https://hideme.eu.org/lookup?api=aadhar-info&key=eris001&aadhar={}"

CREDIT_INFO = {
    "Developer": "@iameris",
    "BUY": "If You Want To Buy Api Contact @iameris"
}


@app.route("/aadhar", methods=["GET"])
def aadhar():
    key = request.args.get("key")
    aadhar = request.args.get("aadhar")

    # 🔐 API KEY
    if key not in VALID_KEYS:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "Invalid API Key",
            **CREDIT_INFO
        })

    # 📱 VALIDATION
    if not aadhar or not aadhar.isdigit() or len(aadhar) != 12:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "Invalid Aadhar number. Please provide a valid 12-digit Aadhar number.",
            **CREDIT_INFO
        })

    try:
        url = EXTERNAL_API.format(aadhar)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return jsonify({
                "SUCCESS": False,
                "MESSAGE": "API Error",
                **CREDIT_INFO
            })

        # 🔥 RAW DATA (NO CHANGE)
        data = response.json()

        # ✅ SUCCESS → direct return
        if data.get("SUCCESS") == True:
            data.pop("DEVELOPER", None)
            data.pop("BUY", None)
            data.pop("key_expiry", None)

            data.update(CREDIT_INFO)
            return jsonify(data)

        # ❌ FAIL → same message
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": data.get("MESSAGE", "No data found for the given Aadhar number."),
            **CREDIT_INFO
        })

    except Exception:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "API Error",
            **CREDIT_INFO
        })


if __name__ == "__main__":
    app.run(debug=True)
