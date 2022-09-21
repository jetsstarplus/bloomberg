import requests

try: 
    from access_token import authentication
    import keys
    from encryption_password import encryptInitiatorPassword
except:  
    from .access_token import authentication
    from . import keys
    from .encryption_password import encryptInitiatorPassword

def ask_balance():
    access_token = authentication()
    encrypted_password = encryptInitiatorPassword()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "Initiator":keys.initiatorName,
        "SecurityCredential":keys.generatedInitiatorSecurityCredential,
        "CommandID":"AccountBalance",
        "PartyA":keys.PartyA,
        "IdentifierType":"4",
        "Remarks":"This is a balance query",
        "QueueTimeOutURL":"https://hilmus-tutor.herokuapp.com/payments/lmmapi/qeuetimeout/",
        "ResultURL":"https://hilmus-tutor.herokuapp.com/payments/lmmapi/balance/"
        }

    try:
        response = requests.post(api_url, json = request, headers=headers)
    except:
        response = requests.post(api_url, json = request, headers=headers, verify=False)

    print (response.text)
    return response
ask_balance()