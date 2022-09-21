import requests

try:
    import keys
    from exceptions import MpesaConnectionError
except:
    from . import keys
    from .exceptions import MpesaConnectionError

#this is the authentication from safaricom
def authentication():
    """This method requests for authentication keys from safaricom"""
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    mpesa_domain = keys.mpesa_domain
    api_URL = "https://{}.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials".format(mpesa_domain)
    
    try:
        r = requests.get(api_URL, auth=(consumer_key, consumer_secret))
        json_token = r.json()
    except Exception:
        raise MpesaConnectionError('Connection Error')
        
    my_access_token = json_token["access_token"]
    # print(json_token)
    return my_access_token
# authentication()
