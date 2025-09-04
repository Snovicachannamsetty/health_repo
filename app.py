from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

# GitHub raw URLs of your files
DISEASES_URL = "https://raw.githubusercontent.com/Snovicachannamsetty/health_repo/main/diseases.json"
SYMPTOMS_URL = "https://raw.githubusercontent.com/Snovicachannamsetty/health_repo/main/symptoms.json"
PREVENTIONS_URL = "https://raw.githubusercontent.com/Snovicachannamsetty/health_repo/main/preventions.json"

# Load JSON data from GitHub
def load_json_from_url(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

diseases_data = load_json_from_url(DISEASES_URL)
symptoms_data = load_json_from_url(SYMPTOMS_URL)
preventions_data = load_json_from_url(PREVENTIONS_URL)


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    intent = req.get("queryResult").get("intent").get("displayName")

    if intent == "disease_info":
        parameters = req.get("queryResult").get("parameters")
        disease = parameters.get("disease_data")
        symptom = parameters.get("symptoms_data")

        response_text = ""

        # If user asks about a disease
        
        if disease:
            # Handle if disease is a list
            if isinstance(disease, list) and len(disease) > 0:
                disease = disease[0]
            disease = disease.lower()

            # Check symptoms
            if disease in symptoms_data:
                symptoms = ", ".join(symptoms_data[disease])
                response_text += f"The common symptoms of {disease.title()} are: {symptoms}. "

            # Check preventions
            if disease in preventions_data:
                preventions = ", ".join(preventions_data[disease])
                response_text += f"Preventions include: {preventions}. "

            if not response_text:
                response_text = f"Sorry, I don’t have data for {disease.title()}."

        # If user asks about a symptom
        elif symptom:
            symptom = symptom.lower()
            matching_diseases = [
                dis for dis, syms in symptoms_data.items() if symptom in [s.lower() for s in syms]
            ]

            if matching_diseases:
                response_text = f"The symptom '{symptom}' is commonly seen in: {', '.join(matching_diseases)}."
            else:
                response_text = f"Sorry, I couldn’t find any disease with the symptom '{symptom}'."

        else:
            response_text = "Please ask me about a disease or symptom."

        return jsonify({"fulfillmentText": response_text})

    return jsonify({"fulfillmentText": "Intent not handled by webhook."})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
