from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VALID_KEYS = ["eris77", "swrovh336"]

EXTERNAL_API = "https://hideme.eu.org/lookup?api=aadhar-info&key=eris001&aadhar={}"

CREDIT_INFO = {
    "Developer": "@iameris",
    "Api": "If You Want To Buy Api Contact @iameris"
}


@app.route("/aadhar", methods=["GET"])
def aadhar():
    key = request.args.get("key")
    aadhar = request.args.get("aadhar")

    # 🔐 API KEY VALIDATION
    if key not in VALID_KEYS:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "Invalid API Key",
            **CREDIT_INFO
        })

    # 📱 AADHAR VALIDATION
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

        try:
            data = response.json()
        except:
            return jsonify({
                "SUCCESS": False,
                "MESSAGE": "Invalid API Response",
                **CREDIT_INFO
            })

        # ✅ SUCCESS CASE
        if data.get("SUCCESS") == True and "RESULTS" in data:
            results = []

            for item in data["RESULTS"]:
                results.append({
                    "ID": str(item.get("ID", "")),
                    "NAME": item.get("NAME", ""),
                    "FNAME": item.get("FNAME", ""),
                    "MOBILE": str(item.get("MOBILE", "")),
                    "ADDRESS": item.get("ADDRESS", ""),
                    "EMAIL": item.get("EMAIL", ""),
                    "ALT": str(item.get("ALT", "")),
                    "CIRCLE": item.get("CIRCLE", "")
                })

            return jsonify({
                "SUCCESS": True,
                "COUNT": len(results),
                "RESULTS": results,
                "Developer": "@iameris",
                "BUY": "If You Want To Buy Api Contact @iameris"
            })

        # ❌ FAIL CASE (same structure)
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": data.get("MESSAGE", "No data found for the given Aadhar number."),
            **CREDIT_INFO
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "API Timeout",
            **CREDIT_INFO
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "SUCCESS": False,
            "MESSAGE": "API Connection Failed",
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