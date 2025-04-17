from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
gsheets_client = gspread.authorize(credentials)

SHEET_NAME = "Leads Consórcio"
TAB_NAME = "Leads"
sheet = gsheets_client.open(SHEET_NAME).worksheet(TAB_NAME)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()

    parameters = req.get("queryResult", {}).get("parameters", {})

    telefone = req.get("originalDetectIntentRequest", {}).get("payload", {}).get("phone", "")
    tipo = parameters.get("tipoConsorcio", "-")
    credito = parameters.get("valorCredito", "-")
    parcela = parameters.get("parcelaIdeal", "-")
    entrada = parameters.get("valorLance", "-")
    contato = parameters.get("formaContato", "-")
    data = datetime.now().strftime("%d/%m/%Y")

    nova_linha = [data, telefone, tipo, credito, parcela, entrada, contato, "Novo Lead"]
    sheet.append_row(nova_linha)

    return jsonify({"fulfillmentText": "Seus dados foram registrados com sucesso. Em breve, nossa equipe entrará em contato."})

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
