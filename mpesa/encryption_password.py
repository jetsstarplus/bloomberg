import base64
try:
    from . import keys
    from .exceptions import *
except:
    import keys
    from exceptions import *
    
# from M2Crypto.M2Crypto import RSA, X509
import os
from base64 import b64encode
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import rsa
from django.conf import settings

#encrypting the data we are using

def data_encryption(formatted_time):
    data_to_encode = keys.LipaNaMpesaOnlineShortcode + keys.LipaNaMpesaOnlinePasskey + formatted_time
    encoded_data = base64.b64encode(data_to_encode.encode())
    #print(encoded_data)
    decoded_password = encoded_data.decode('utf-8')
    # print(str(decoded_password))
    return decoded_password

  
def encrypt_security_credential(credential):
	"""
	Generate an encrypted security credential from a plaintext value
	
	Arguments:
		credential (str) -- The plaintext credential display
	"""

	mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')

	if mpesa_environment in ('sandbox', 'production'):
		certificate_name = mpesa_environment + '.cer'
	else:
		raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

	certificate_path = os.path.join(settings.BASE_DIR, 'certs', certificate_name)
	return encrypt_rsa(certificate_path, credential)

def encryptInitiatorPassword():
    """A method that encrypts the initiater password with the certificate file"""
    with open(keys.CERTIFICATE_FILE, 'rb') as cert_file:
        cert_data = cert_file.read() #read certificate file

    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    #pub_key = X509.load_cert_string(cert_data)
    pub_key = cert.public_key().public_numbers()
    # print(pub_key)
    cipher = rsa.encrypt(keys.INITIATOR_PASS.encode(), pub_key)
    # print(b64encode(cipher))
    
    return b64encode(cipher).decode('utf-8')

# def encrypt_rsa(certificate_path, input):
#     message = input.encode('ascii')
#     with open(certificate_path, "rb") as cert_file:
# 		cert = x509.load_pem_x509_certificate(cert_file.read())
# 		encrypted = cert.public_key().encrypt(message, PKCS1v15())
# 		output = base64.b64encode(encrypted).decode('ascii')

# 	return output
# encryptInitiatorPassword()
