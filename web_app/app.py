
from flask import Flask, flash, redirect, render_template, request, session, abort
import urllib.request as req
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import os

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.gdax.com/'
app = Flask(__name__)

API_KEY ='your_api_key'
SECRET_KEY = 'your_secret_key'
PASSPHRASE = 'your_passphrase'


@app.route('/')
def hello_world():

    if not session.get('logged_in'):
        return render_template("login.html")
    else: 

        auth = CoinbaseExchangeAuth(API_KEY, SECRET_KEY, PASSPHRASE)

        r = requests.get(api_url + 'accounts', auth=auth)

        data_ltc=str(req.urlopen("https://api.gdax.com/products/LTC-EUR/book?level=2").read())

        processed_data_ltc = json.loads(data_ltc[2:-1])

        current_price_ltc = processed_data_ltc["bids"][0][0]

        data_btc=str(req.urlopen("https://api.gdax.com/products/BTC-EUR/book?level=2").read())

        processed_data_btc = json.loads(data_btc[2:-1])

        current_price_btc = processed_data_btc["bids"][0][0]

        data_eth=str(req.urlopen("https://api.gdax.com/products/ETH-EUR/book?level=2").read())

        processed_data_eth = json.loads(data_eth[2:-1])

        current_price_eth = processed_data_eth["bids"][0][0]


        data_eth_btc=str(req.urlopen("https://api.gdax.com/products/ETH-BTC/book?level=2").read())

        processed_data_eth_btc = json.loads(data_eth_btc[2:-1])

        current_price_eth_btc = processed_data_eth_btc["bids"][0][0]

        amount_invested = 0

        id_account_eur = ""

        current_amount_btc = 0

        for element in r.json():
            if "BTC" == element['currency']:
                current_amount_btc=float(element['balance'])
            if "ETH" == element['currency']:
                current_amount_eth=float(element['balance'])
            if "LTC" == element['currency']:
                current_amount_ltc=float(element['balance'])
            if "EUR" == element['currency']:
                current_amount_eur = float(element['balance'])
                id_account_eur = element['id']

        funding_history = requests.get(api_url + 'accounts/'+id_account_eur+'/ledger',auth=auth)

        for movement in funding_history.json():
    	    if movement['type'] == 'transfer':
    		    amount_invested+=float(movement['amount'])

          

        #total investments value (euros)
        current_profits=(float(current_price_btc)*(current_amount_btc)+float(current_price_ltc)*(current_amount_ltc)+float(current_price_eth)*(current_amount_eth)+current_amount_eur)-amount_invested

        profit_formatted = "{:{width}.{prec}f} €".format(current_profits,width=8,prec=2)       

        message = "Current profits: "+profit_formatted

        

        imagen_ganancias = 'http://klaithal.altervista.org/imagenes/ganancias.png'

        imagen_perdidas = 'http://klaithal.altervista.org/imagenes/perdidas.png'

        if current_profits < 0:
            imagen_a_mostrar = imagen_perdidas
            smiley = " :-("
        else:
            imagen_a_mostrar = imagen_ganancias
            smiley = " :-D"

        return render_template("index.html",profit=(profit_formatted+smiley), message=message, imagen_a_mostrar=imagen_a_mostrar, btc_eth_ratio=btc_eth_ratio)
        


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'some_password' and request.form['username'] == 'your_name':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return hello_world()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return hello_world()



if __name__ == "__main__":
    app.secret_key=os.urandom(15)    
    app.run(debug=False)