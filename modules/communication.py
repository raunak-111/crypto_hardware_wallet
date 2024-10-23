import base64
def store_key_to_usb(usb_path, nonce, ciphertext, tag):
    with open(usb_path+'/key/pri_key.pem', 'wb') as f:
        f.write(base64.b64encode(nonce + ciphertext + tag))

def retrieve_key_from_usb(usb_path, aes_key):
    from .key_management import KeyManagement
    with open(usb_path+'/key/pri_key.pem', 'rb') as f:
        data = base64.b64decode(f.read())
        nonce, ciphertext, tag = data[:16], data[16:-16], data[-16:]

        
    
    km = KeyManagement(aes_key)
    decrypted_key = km.decrypt_key(nonce, ciphertext, tag)
    return decrypted_key
