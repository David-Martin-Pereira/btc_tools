# btc_tools
Tools for monitoring bitcoin


The first, "web_app" is a flask application that connect to your gdax API to tell you whether or not you are wining money with your investment.

To use it, you would need:

- Python3 with the following packages installed
  - Flask
  - requests
 
- A gdax account and API key. Just follow these instructions: https://docs.gdax.com/#generating-an-api-key

- Update the values of API_KEY, SECRET_KEY and PASSPHRASE in the app.py

- Optionally, update your user and password in the login methods.

- Once installed, copy, run it with:

  python3 web_app/app.py
  
  And you can test it at localhost:5000
  
  
 
 It updates itself every 5 minutes.
 
 Of course, you can deploy it wherever.
