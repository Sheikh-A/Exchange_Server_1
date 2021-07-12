from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

# {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c',
#  'payload':
#    {'message': 'Ethereum test message',
#     'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF',
#     'platform': 'Ethereum'}}


@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)

    payload = content["payload"]
    print(payload)

    pk = payload["pk"]
    print(pk)

    sig = content["sig"]
    print(sig)

    message = payload["message"]
    print(message)

    platform = payload["platform"]
    print(platform)

    result = False

    if platform == "Algorand":
        algo_sig = sig
        algo_pk = pk
        if algosdk.util.verify_bytes(json.dumps(payload).encode('utf-8'),algo_sig,algo_pk):
            result = True

    elif platform == "Ethereum":
        eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(payload))
        eth_recover = eth_account.Account.recover_message(eth_encoded_msg, signature=sig)
        eth_pk = payload["pk"]
        if eth_pk==eth_recover:
            result = True
    else:
        print("Please use Algorand or Ethereum ONLY")
        result = False


    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
