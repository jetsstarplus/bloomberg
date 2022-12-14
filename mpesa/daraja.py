
import requests

try:
    #other libraries import
    from access_token import authentication
    import keys
    from encryption_password import data_encryption
    from utils import timestamp
except:
    #other libraries import
    from .access_token import authentication
    from . import keys
    from .encryption_password import data_encryption
    from .utils import timestamp




#create the lipa na mpesa API
def lipa_na_mpesa(phone_number, amount, account, transaction):

    access_token = authentication()
    mpesa_domain = keys.mpesa_domain
    api_url = "https://{}.safaricom.co.ke/mpesa/stkpush/v1/processrequest".format(mpesa_domain)
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "BusinessShortCode": keys.LipaNaMpesaOnlineShortcode,
        "Password": data_encryption(timestamp()),
        "Timestamp": timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA":phone_number,
        "PartyB":keys.LipaNaMpesaOnlineShortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": keys.lipa_na_mpesa_callback_url,
        "AccountReference": account,
        "TransactionDesc": transaction
    }

    #sending the request and expecting back a response
    try:
        response = requests.post(api_url, json = request, headers=headers, stream=True)
    except:
        response = requests.post(api_url, json = request, headers=headers, verify=False, stream=True)

    # print (response.text)
    return(response)
# print(lipa_na_mpesa('254701850242', '1', '123488', "trial instance").text)
