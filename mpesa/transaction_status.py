import requests

from access_token import authentication

access_token = authentication()

headers = {

  'Content-Type': 'application/json',

  'Authorization': 'Bearer %s' % access_token

}


payload = {

    "initiator": "testapi",

    "SecurityCredential": "tuCWKyGlBdpvvQ/4ZcFS/N3kJnL85aBnb7OXvErcJjteN6igrGdOgbWFY3Q14RIRFxPHLP9y8zOSTeyo91K5+it/YsmVim5DZx4rT51nKy7Z8NWXScYu/7Vhh1mHJpvYNPCXdfnwD6Xo9lE8bqS4Y0UpFUeux658tB1ia4WFcx9lg67DE81B1SYWHWuT5ek9LqYN7SBbMTe18d10+M38Rs8S4tYAEk2/69oUjha+dsiAJBvkJRLCmAI2ewNXzHQPINci00a3ImZ3zUtw2m2o8b55+FB+FEPt7FncVtXr4kE/l8CpP8zvivkzqRS3q0lAhekcDSZgGjwFlt9rTmGMlw==",

    "CommandID": "TransactionStatusQuery",

    "TransactionID": "OEI2AK4Q16",

    "PartyA": 600994,

    "IdentifierType": "1",

    "ResultURL": "https://hilmus-tutor.herokuapp.com/TransactionStatus/result/",

    "QueueTimeOutURL": "https://hilmus-tutor.herokuapp/TransactionStatus/queue/",

    "Remarks": "sdad",

    "Occassion": "sdssd",

  }

response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query', headers = headers, data = payload)

print(response.text.encode('utf8'))

