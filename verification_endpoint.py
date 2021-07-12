from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False


@app.route('/')
def home():
    return "Hello this is the main page <h1>HELLO<h1>"

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"


@app.route('/verify', methods=['GET','POST'])

# {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c',
#  'payload':
#    {'message': 'Ethereum test message',
#     'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF',
#     'platform': 'Ethereum'}}


def verify():
    content = request.get_json(silent=True)

    platform = content["payload"]["platform"]
    msg = content["payload"]["message"]
    pk = content["payload"]["pk"]
    sig = content["sig"]
    payload = content["payload"]

    #Check if signature is valid
    result = False #Should only be true if signature validates

    #Algorand Case
    if platform == 'Algorand':
        algo_pk = payload["pk"]
        algo_sig = content["sig"]
        if algosdk.util.verify_bytes(msg.encode('utf-8'), sig, pk):
            result = True
        else:
            result = False
    elif platform == 'Ethereum':
        eth_encoded_msg = eth_account.messages.encode_defunct(text=msg)
        eth_recover = eth_account.Account.recover_message(eth_encoded_msg, signature=sig)
        if eth_recover == pk:
            result = True
        else:
            result = False
    else:
        print("Please use Algorand or Ethereum")
        result = False

    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
