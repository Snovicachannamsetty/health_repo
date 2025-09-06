'''from flask import Flask, request, jsonify
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
    return response.json() if response.status_code == 200 else []


# Convert list of dicts into lookup dictionaries
def build_lookup(data, key, value_key):
    lookup = {}
    for item in data:
        if key in item and value_key in item:
            lookup[item[key].lower()] = item[value_key]
    return lookup


# Load files
diseases_raw = load_json_from_url(DISEASES_URL)
symptoms_raw = load_json_from_url(SYMPTOMS_URL)
preventions_raw = load_json_from_url(PREVENTIONS_URL)

# Convert into dictionaries
symptoms_data = build_lookup(symptoms_raw, "value", "symptoms")
preventions_data = build_lookup(preventions_raw, "value", "preventions")
disease_names = [d["value"].lower() for d in diseases_raw] if diseases_raw else []


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
            if isinstance(disease, list) and len(disease) > 0:
                disease = disease[0]
            disease = disease.lower()

            if disease in symptoms_data:
                symptoms = ", ".join(symptoms_data[disease])
                response_text += f"The common symptoms of {disease.title()} are: {symptoms}. "

            if disease in preventions_data:
                preventions = ", ".join(preventions_data[disease])
                response_text += f"Preventions include: {preventions}. "

            if not response_text:
                response_text = f"Sorry, I don’t have data for {disease.title()}."

        # If user asks about a symptom
        elif symptom:
            if isinstance(symptom, list) and len(symptom) > 0:
                symptom = symptom[0]
            symptom = symptom.lower()

            matching_diseases = [
                dis.title() for dis, syms in symptoms_data.items()
                if symptom in [s.lower() for s in syms]
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
    app.run(host="0.0.0.0", port=port)'''



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
    return response.json() if response.status_code == 200 else []


# Convert list of dicts into lookup dictionaries
def build_lookup(data, key, value_key):
    lookup = {}
    for item in data:
        if key in item and value_key in item:
            lookup[item[key].lower()] = item[value_key]
    return lookup


# Load files
diseases_raw = load_json_from_url(DISEASES_URL)
symptoms_raw = load_json_from_url(SYMPTOMS_URL)
preventions_raw = load_json_from_url(PREVENTIONS_URL)

# Convert into dictionaries
symptoms_data = build_lookup(symptoms_raw, "value", "symptoms")
preventions_data = build_lookup(preventions_raw, "value", "preventions")
disease_names = [d["value"].lower() for d in diseases_raw] if diseases_raw else []


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    intent = req.get("queryResult").get("intent").get("displayName")

    # -------- Disease Info Intent --------
    if intent == "disease_info":
        parameters = req.get("queryResult").get("parameters")
        disease = parameters.get("disease_data")
        symptom = parameters.get("symptoms_data")

        response_text = ""

        # If user asks about a disease
        if disease:
            if isinstance(disease, list) and len(disease) > 0:
                disease = disease[0]
            disease = disease.lower()

            if disease in symptoms_data:
                symptoms = ", ".join(symptoms_data[disease])
                response_text += f"The common symptoms of {disease.title()} are: {symptoms}. "

            if disease in preventions_data:
                preventions = ", ".join(preventions_data[disease])
                response_text += f"Preventions include: {preventions}. "

            if not response_text:
                response_text = f"Sorry, I don’t have data for {disease.title()}."

        # If user asks about a symptom
        elif symptom:
            if isinstance(symptom, list) and len(symptom) > 0:
                symptom = symptom[0]
            symptom = symptom.lower()

            matching_diseases = [
                dis.title() for dis, syms in symptoms_data.items()
                if symptom in [s.lower() for s in syms]
            ]

            if matching_diseases:
                response_text = f"The symptom '{symptom}' is commonly seen in: {', '.join(matching_diseases)}."
            else:
                response_text = f"Sorry, I couldn’t find any disease with the symptom '{symptom}'."

        else:
            response_text = "Please ask me about a disease or symptom."

        return jsonify({"fulfillmentText": response_text})

    # -------- Preventions Info Intent --------
    elif intent == "prevention_info":
        parameters = req.get("queryResult").get("parameters")
        disease = parameters.get("disease_data")

        response_text = ""

        if disease:
            if isinstance(disease, list) and len(disease) > 0:
                disease = disease[0]
            disease = disease.lower()

            if disease in preventions_data:
                preventions = ", ".join(preventions_data[disease])
                response_text = f"Preventions for {disease.title()} are: {preventions}."
            else:
                response_text = f"Sorry, I don’t have prevention info for {disease.title()}."
        else:
            response_text = "Please specify a disease to get prevention information."

        return jsonify({"fulfillmentText": response_text})

    # -------- Default Fallback --------
    return jsonify({"fulfillmentText": "Intent not handled by webhook."})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
