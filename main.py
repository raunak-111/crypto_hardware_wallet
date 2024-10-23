import os
from modules import *
from ecdsa import SigningKey,SECP256k1
from Crypto.Random import get_random_bytes

#Task-
#1-Main function task is to generate the private key using ecdsa-we are using ecdsa because  bitcoin and ethereum used ecdsa .
#2-encrypt the private key using AES.
#3- Store the encrypted private key in a USB.
#4- Retrieve the encrypted private key from the USB.
#5- Decrypt the encrypted private key using AES.
#6- Sign the transaction.


#Generate private and public key using ecdsa
def generate_private_and_public_key():
    private_key = SigningKey.generate(curve=SECP256k1)
    private_key_hex = private_key.to_string().hex()
    public_key_hex = private_key.get_verifying_key().to_string().hex()
    return private_key_hex, public_key_hex
def main():
    print("Generating private key.....")
    private_key, public_key = generate_private_and_public_key()
    print("Generated Private key: ", private_key)
    print("Generated Public key: ", public_key)


    #Task-2 Encrypt the private key using AES encryption.
    print("Encrypting private key....")
    aes_key = get_random_bytes(16) # generate a 16-byte  AES key
    km = KeyManagement(aes_key)
    nonce ,ciphertext,tag = km.encrypt(private_key)
    


    #Task-3 Store the encrypted private key in a USB.
    print("Storing encrypted private key in USB....")
    usb_path= '/media/aryandev/GPARTED-LIV'
    print("Storing encrypted private key in ", usb_path)
    store_key_to_usb(usb_path, nonce, ciphertext, tag)
    print(f"Encrypted private key stored in {usb_path}")


    #Task-4 Retrieve the encrypted private key from the USB.
    print("Retrieving encrypted private key from USB....")
    retrieved_key = retrieve_key_from_usb(usb_path,aes_key)
    print("Retrieved encrypted private key: ", retrieved_key)

    # Step 5: Sign a transaction using the decrypted private key
    print("Signing a transaction...")
    transaction_data = "Alice sent 10 BTC to Bob"
    signature = sign_transaction(retrieved_key, transaction_data)
    print(f"Transaction Signature: {signature.hex()}")




if __name__ == "__main__":
    main()