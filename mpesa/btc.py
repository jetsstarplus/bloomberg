import requests

from access_token import authentication
from encryption_password import encryptInitiatorPassword
import keys

access_token = authentication()
url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
security_credential = encryptInitiatorPassword()
print(security_credential)
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer %s' % access_token,
}

payload = {
    "InitiatorName": keys.initiatorName,
    "SecurityCredential": keys.generatedInitiatorSecurityCredential,
    "CommandID": "SalaryPayment",
    "Amount": 1,
    "PartyA": keys.PartyA,
    "PartyB": keys.TestMSISDN,
    "Remarks": "Test remarks",
    "QueueTimeOutURL": "https://hilmus-tutor.herokuapp.com/payments/b2c/queue/timeout/",
    "ResultURL": "https://hilmus-tutor.herokuapp.com/payments/b2c/result/",
    "Occassion": "This is the occassion",
  }
try:
  response = requests.post(url = url, headers = headers, data = payload)
except:
  response = requests.post(url = url, headers = headers, data = payload, verify=False)
print(response.text)
