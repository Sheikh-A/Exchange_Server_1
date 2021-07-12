from flask import Flask, request, jsonify, redirect, url_for
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False


# @app.route('/')
# def home():
#     return "Hello this is the main page <h1>HELLO<h1>"

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

    sig = content["sig"]
    pk = content["payload"]["pk"]
    msg = content["payload"]["message"]
    platform = content["payload"]["platform"]
    result = True
    if platform == 'Ethereum':
        eth_encoded_msg = eth_account.messages.encode_defunct(text=msg)
        if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
            result = True
        else:
            result = False
    else:
        if algosdk.util.verify_bytes(msg.encode('utf-8'),sig,pk):
            result = True
        else:
            result = False
    #Check if signature is valid
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
