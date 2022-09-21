#in this file we register our url to safaricon

import requests

# for testing and django functionality
try:
    from .access_token import authentication        
    from . import keys
except:
    from access_token import authentication        
    import keys


access_token = authentication()

def register_url():
    mpesa_domain = keys.mpesa_domain
    api_url = "https://{}.safaricom.co.ke/mpesa/c2b/v1/registerurl".format(mpesa_domain)
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "ShortCode":keys.business_shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": keys.c2b_confirmation_url,
        "ValidationURL": keys.c2b_validation_url}

    try:
        response = requests.post(api_url, json = request, headers=headers)
    except:
         response = requests.post(api_url, json = request, headers=headers, verify=False)   

    print (response.text)
    
register_url()
