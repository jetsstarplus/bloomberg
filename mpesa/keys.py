import os

business_shortcode= os.getenv('businessShortcode',default='174379')
SecurityCredential= "YbXpYqLevyQNnmIRR"
PartyA = "601393"
PartyB = "600000"
LipaNaMpesaOnlineShortcode= os.getenv('MPESASHORTCODE',default='174379')
LipaNaMpesaOnlinePasskey=os.getenv('MPESAPASSKEY', default='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
TestMSISDN = "254708374149"
initiatorName = "testapi"

#authentication credentials
consumer_key =os.getenv('CONSUMERKEY', default='YLzDDzJAx8mVh5u2TfpNgoPGBHxaOF1U')
consumer_secret =os.getenv('CONSUMERSECRET', default='7asxP6Ce511DLDH7')
generatedInitiatorSecurityCredential = "fFck10GKsYNZexcaIYfUVq+PrCuCkW+vsN5bhA+A0z7Nt7KF468zPM7iHeaUzOOLISWSWcYuQUbmHWiEtFDJAneMoZjLgdWlPjU0NGTRHWrODrfGIFmiJThp2Q6fPPXl6blpx0ixHUnoHND65EcR7DFjZBbAyc1OcrKOV/R913aeusLf1O8/DsQUWEv8tGqGC3Tp/vIOIi9ekNcfEHqu90yGoUgPx/FL6cU9rOJqKas4CZ+1NZiwMZN0L7lLNT3c6uAAy98mJGLk+QWXIGP2Eep7L5CGmzKggogjcRU+QxM6//t1FIMU0uGTNZJ2WFqTnTQy3r2M/uvP7Q+9ZaFztA=="
mpesa_domain = os.getenv('MPESADOMAIN', default = 'sandbox')
#shortcode encryption
INITIATOR_PASS  = "Safaricom983!#"
CERTIFICATE_FILE = "mpesa/SandboxCertificate.cer"

# url configuration
lipa_na_mpesa_callback_url = os.getenv('LIPANAMPESACALLBACKURL', default = 'https://hilmus-tutor.herokuapp.com:8000/payments/lmmapi/')
c2b_confirmation_url= os.getenv('C2BCONFIRMATIONURL', default = "https://localhost:8000/payments/lmmapi/confirm/")
c2b_validation_url=os.getenv('C2BVALIDATIONURL', default= "https://localhost:8000/payments/lmmapi/validate/")
