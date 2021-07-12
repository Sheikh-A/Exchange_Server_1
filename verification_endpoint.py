from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    payl = content["payload"]
    platform = payl['platform']
    result = False

    if platform == "Ethereum":
        eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(payl))
        eth_recover = eth_account.Account.recover_message(eth_encoded_msg, signature=content["sig"])
        eth_pk = payl["pk"]
        if eth_recover==eth_pk:
            result = True

    if platform == "Algorand":
        algo_pk = payl["pk"]
        algo_sig = content["sig"]
        if algosdk.util.verify_bytes(json.dumps(payl).encode('utf-8'),algo_sig,algo_pk):
            result = True

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
