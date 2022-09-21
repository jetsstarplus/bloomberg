import requests

try:
  import keys
  from access_token import authentication
except:
  from . import keys
  from .access_token import authentication

access_token = authentication()


#register_url()
def simulate_transaction():
  mpesa_domain = keys.mpesa_domain  
  api_url = "https://{}.safaricom.co.ke/mpesa/c2b/v1/simulate".format(mpesa_domain)
  headers = {"Authorization": "Bearer %s" % access_token}
  request = { "ShortCode":keys.business_shortcode,
    "CommandID":"CustomerPayBillOnline",
    "Amount":"1000",
    "Msisdn":keys.TestMSISDN,
    "BillRefNumber":"12345678" }
  
  try:
    response = requests.post(api_url, json = request, headers=headers)
  except:
    response = requests.post(api_url, json = request, headers=headers, verify=False)
  
  
  print (response.text)

simulate_transaction()
