import os
from modules import *
from ecdsa import SigningKey,SECP256k1
from Crypto.Random import get_random_bytes
import json
import random
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

#Task-
#1-Main function task is to generate the private key using ecdsa-we are using ecdsa because  bitcoin and ethereum used ecdsa .
#2-encrypt the private key using AES.
#3- Store the encrypted private key in a USB.
#4- Retrieve the encrypted private key from the USB.
#5- Decrypt the encrypted private key using AES.
#6- Sign the transaction.
# A mock seed phrase list (for simplicity, using a smaller set of words)
seed_words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", 
              "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", 
              "strawberry", "tomato", "ugli", "vanilla", "watermelon", "xigua", "yam", "zucchini"]


def derive_aes_key(pin, salt):
    return PBKDF2(pin, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)

# Function to generate a seed phrase
def generate_seed_phrase():
    seed_phrase = random.sample(seed_words, 4)  # Use 12 words for simplicity
    print("\n--- Your Seed Phrase ---")
    print("Write down the following seed phrase in the correct order:\n")
    for idx, word in enumerate(seed_phrase):
        print(f"{idx + 1}: {word}")
    print("\nStore this securely. This will not be shown again.")
    return seed_phrase

# Function to verify the seed phrase
def verify_seed_phrase(seed_phrase):
    print("\n--- Verifying Seed Phrase ---")
    print("Please enter the words in the correct order.")
    for idx in range(len(seed_phrase)):
        user_input = input(f"Enter word {idx + 1}: ").strip()
        if user_input != seed_phrase[idx]:
            print("Verification failed! Seed phrase does not match.")
            return False
    print("Seed phrase verified successfully!")
    return True
# Function to set up a PIN for the wallet

def set_pin():
    print("\n--- Setting Up PIN ---")
    while True:
        pin = getpass("Enter a 4-digit PIN: ").strip()
        pin_confirm = getpass("Confirm your 4-digit PIN: ").strip()
        if len(pin) == 4 and pin == pin_confirm:
            print("PIN setup successful!")
            return pin
        else:
            print("PINs do not match or not 4 digits. Try again.")
# Function to complete the wallet creation
def create_new_wallet(usb_path):
    print("\n--- Create New Wallet ---")

    # Step 1: Generate Seed Phrase
    seed_phrase = generate_seed_phrase()

    # Step 2: Verify Seed Phrase
    if not verify_seed_phrase(seed_phrase):
        print("Wallet creation failed due to incorrect seed phrase.")
        return

    # Step 3: Set PIN
    pin = set_pin()

    # Step 4: Create Wallet (Generate private and public key)
    private_key = SigningKey.generate(curve=SECP256k1)
    private_key_hex = private_key.to_string().hex()
    public_key_hex = private_key.get_verifying_key().to_string().hex()
    print("private key:",private_key_hex)
  

   
    #Step 5: Derive AES key from the PIN using a salt
    salt = get_random_bytes(16)
    aes_key = derive_aes_key(pin, salt)

    # Step 5: Encrypt private key and store wallet
    print("\nEncrypting private key for secure storage...")
    km = KeyManagement(aes_key)
    nonce, ciphertext, tag = km.encrypt(private_key_hex)

    # Save wallet info to USB
    wallet_file_path = os.path.join(usb_path, "wallet.json")
    wallet_info = {
        "seed_phrase": seed_phrase,  # Seed phrase (should be stored securely)
        "public_key": public_key_hex,
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex(),
        "tag": tag.hex(),
        "salt": salt.hex(),
    }

    with open(wallet_file_path, 'w') as wallet_file:
        json.dump(wallet_info, wallet_file)
    print("\n--- Wallet Created Successfully ---")
    print(f"Wallet information stored in {wallet_file_path}")
    client_socket.close()
    server_socket.close()

# Function to load the wallet (similar to previous)
def load_wallet_with_pin(usb_path):
    wallet_file_path = os.path.join(usb_path, "wallet.json")
    # Check if wallet exists
    if not os.path.exists(wallet_file_path):
        print("No wallet found. Please create a wallet first.")
        return None
    with open(wallet_file_path, 'r') as wallet_file:
        encrypted_wallet = json.load(wallet_file)
    # Verify PIN before decrypting private key
     # Wait for the response from the mobile device
     # Function to derive AES key from the PIN using PBKDF2
    client_socket, address, server_socket = bluetooth_server()
    print("Enter pin to sign the transaction:")
    
    pin = client_socket.recv(1024).decode('utf-8')
    
    print(f"Received PIN from mobile device: {pin}")
    client_socket.close()
    server_socket.close()

    # Derive AES key from the PIN and salt
    salt = bytes.fromhex(encrypted_wallet['salt'])
    aes_key = derive_aes_key(pin, salt)
    try:
        # Decrypt private key
        km = KeyManagement(aes_key)
        private_key_hex = km.decrypt_key(
            bytes.fromhex(encrypted_wallet['nonce']),
            bytes.fromhex(encrypted_wallet['ciphertext']),
            bytes.fromhex(encrypted_wallet['tag'])
        )
    except ValueError:
        print("Decryption failed: MAC check failed. Please try again. Incorrect PIN?")
        return None
    wallet_info = {
        "seed_phrase": encrypted_wallet['seed_phrase'],
        "public_key": encrypted_wallet['public_key'],
        "private_key": private_key_hex  # Decrypted private key
    }
    print(f"Wallet with public key {wallet_info['public_key']} loaded successfully!")

    return wallet_info




def main():
    usb_path = '/media/aryandev/GPARTED-LIV'
    
    while True:
        display_menu()
        choice = input("Please select an option (1-3): ").strip()
        if choice == '1':
            create_new_wallet(usb_path)
        elif choice == '2':
            wallet_info = load_wallet_with_pin(usb_path)
            if wallet_info:
                # Example transaction signing using the loaded wallet
                transaction_data = "Alice sent 10 BTC to Bob"
                signature = sign_transaction(wallet_info["private_key"], transaction_data)
                print(f"Transaction Signature: {signature.hex()}")
        elif choice == '3':
            print("Exiting the wallet dashboard. Goodbye!")
            break
        else:
            print("Invalid option. Please select a valid option (1-3).")



    
if __name__ == "__main__":
    main()