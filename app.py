from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AdShield</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 650px;
                max-width: 90%;
                margin: 60px auto;
                background: white;
                padding: 35px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.12);
            }

            h1 {
                text-align: center;
                margin-bottom: 5px;
            }

            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 25px;
            }

            textarea {
                width: 100%;
                height: 160px;
                padding: 15px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 10px;
                resize: none;
                font-size: 15px;
            }

            button {
                width: 100%;
                margin-top: 15px;
                padding: 14px;
                border: none;
                border-radius: 10px;
                background: #222;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background: #444;
            }

            #result {
                margin-top: 25px;
                padding: 20px;
                border-radius: 10px;
                display: none;
            }

            .low {
                background: #e5f7e5;
                color: #176b17;
            }

            .medium {
                background: #fff4cc;
                color: #8a6500;
            }

            .high {
                background: #ffe5e5;
                color: #b00020;
            }

            .score {
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }

            .section {
                margin-top: 18px;
            }

            .section-title {
                font-weight: bold;
                margin-bottom: 8px;
            }

            ul {
                margin-top: 8px;
            }

            li {
                margin-bottom: 5px;
            }

            .explanation {
                margin-top: 15px;
                padding: 12px;
                background: rgba(255,255,255,0.5);
                border-radius: 8px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🛡️ AdShield</h1>

            <p class="subtitle">
                Detect suspicious and potentially misleading advertisements
            </p>

            <textarea id="adText"
                placeholder="Paste advertisement text here..."></textarea>

            <button onclick="checkAd()">
                Check Advertisement
            </button>

            <div id="result"></div>

        </div>


        <script>

            async function checkAd() {

                const text = document.getElementById("adText").value;
                const result = document.getElementById("result");

                if (!text.trim()) {

                    result.style.display = "block";
                    result.className = "high";

                    result.innerHTML =
                        "<strong>Please enter advertisement text.</strong>";

                    return;
                }

                try {

                    const response = await fetch("/check", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    });

                    const data = await response.json();

                    result.style.display = "block";

                    if (data.risk_level === "High Risk") {

                        result.className = "high";

                    } else if (data.risk_level === "Medium Risk") {

                        result.className = "medium";

                    } else {

                        result.className = "low";
                    }


                    let wordsHTML = "";

                    if (data.matched_words.length > 0) {

                        wordsHTML = `
                            <div class="section">
                                <div class="section-title">
                                    Suspicious phrases detected:
                                </div>

                                <ul>
                                    ${data.matched_words.map(word =>
                                        `<li>${word}</li>`
                                    ).join("")}
                                </ul>
                            </div>
                        `;

                    } else {

                        wordsHTML = `
                            <div class="section">
                                <strong>
                                    No suspicious phrases detected.
                                </strong>
                            </div>
                        `;
                    }


                    let riskFactorsHTML = "";

                    if (data.risk_factors.length > 0) {

                        riskFactorsHTML = `
                            <div class="section">
                                <div class="section-title">
                                    ⚠️ Risk Factors
                                </div>

                                <ul>
                                    ${data.risk_factors.map(factor =>
                                        `<li>${factor}</li>`
                                    ).join("")}
                                </ul>
                            </div>
                        `;

                    } else {

                        riskFactorsHTML = `
                            <div class="section">
                                <div class="section-title">
                                    ⚠️ Risk Factors
                                </div>

                                <p>
                                    No major risk factors were identified.
                                </p>
                            </div>
                        `;
                    }


                    result.innerHTML = `
                        <strong>🛡️ AdShield Analysis</strong>

                        <div class="score">
                            Risk Score: ${data.risk_score}/100
                        </div>

                        <strong>${data.risk_level}</strong>

                        <p>${data.message}</p>

                        ${wordsHTML}

                        ${riskFactorsHTML}

                        <div class="explanation">
                            <div class="section-title">
                                💡 Why was this flagged?
                            </div>

                            <p>
                                ${data.explanation}
                            </p>
                        </div>
                    `;

                } catch (error) {

                    result.style.display = "block";
                    result.className = "high";

                    result.innerHTML = `
                        <strong>
                            Something went wrong while checking the advertisement.
                        </strong>
                    `;
                }
            }

        </script>

    </body>
    </html>
    """


@app.route("/check", methods=["POST"])
def check_ad():

    data = request.get_json()

    if not data or "text" not in data:

        return jsonify({
            "error": "Please provide ad text"
        }), 400


    text = data["text"].lower()


    suspicious_words = {

        "free money": 20,
        "guaranteed": 15,
        "click now": 15,
        "limited time": 10,
        "winner": 10,
        "you won": 15,
        "claim now": 15,
        "urgent": 10,
        "act now": 10,
        "risk free": 15,
        "100% guaranteed": 20,
        "exclusive offer": 10

    }


    found_words = []
    risk_score = 0


    for word, points in suspicious_words.items():

        if word in text:

            found_words.append(word)
            risk_score += points


    risk_score = min(risk_score, 100)


    risk_factors = []


    if "free money" in text or "guaranteed" in text or "risk free" in text:

        risk_factors.append(
            "Money-related or unrealistic financial claims"
        )


    if (
        "click now" in text
        or "limited time" in text
        or "urgent" in text
        or "act now" in text
    ):

        risk_factors.append(
            "Urgency or pressure tactics"
        )


    if (
        "winner" in text
        or "you won" in text
        or "claim now" in text
    ):

        risk_factors.append(
            "Prize, winner or reward claims"
        )


    if "exclusive offer" in text:

        risk_factors.append(
            "Promotional or exclusivity language"
        )


    if risk_score >= 50:

        risk_level = "High Risk"

        message = (
            "This advertisement contains several suspicious "
            "patterns and should be treated with caution."
        )


    elif risk_score >= 20:

        risk_level = "Medium Risk"

        message = (
            "This advertisement contains some potentially "
            "misleading or suspicious language."
        )


    else:

        risk_level = "Low Risk"

        message = (
            "No major suspicious advertising patterns were detected."
        )


    if risk_factors:

        explanation_parts = []

        if "Money-related or unrealistic financial claims" in risk_factors:

            explanation_parts.append(
                "it contains financial or unrealistic promises"
            )

        if "Urgency or pressure tactics" in risk_factors:

            explanation_parts.append(
                "it uses urgency or pressure to encourage immediate action"
            )

        if "Prize, winner or reward claims" in risk_factors:

            explanation_parts.append(
                "it uses prize or reward language that may manipulate the user"
            )

        if "Promotional or exclusivity language" in risk_factors:

            explanation_parts.append(
                "it uses promotional language to create a sense of exclusivity"
            )


        if len(explanation_parts) == 1:

            explanation = (
                "The advertisement was flagged because "
                + explanation_parts[0]
                + "."
            )

        elif len(explanation_parts) == 2:

            explanation = (
                "The advertisement was flagged because "
                + explanation_parts[0]
                + " and "
                + explanation_parts[1]
                + "."
            )

        else:

            explanation = (
                "The advertisement was flagged because "
                + ", ".join(explanation_parts[:-1])
                + ", and "
                + explanation_parts[-1]
                + "."
            )

    else:

        explanation = (
            "The advertisement does not contain major suspicious "
            "patterns from the current detection rules."
        )


    return jsonify({

        "risk_score": risk_score,

        "risk_level": risk_level,

        "matched_words": found_words,

        "risk_factors": risk_factors,

        "message": message,

        "explanation": explanation

    })


if __name__ == "__main__":

    app.run(debug=True)