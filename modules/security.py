# Configure logging
import os
import random
import logging
import shutil
logging.basicConfig(filename='security.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def destroy_wallet(wallet_path):    
    WALLET_FILE_PATH = os.path.join(wallet_path, "wallet.json")
   

    # Option 1: Overwrite file with different patterns, then delete
    if os.path.exists(WALLET_FILE_PATH):
        try:
            # Redundant overwriting with different patterns
            for _ in range(3):  # Three passes
                with open(WALLET_FILE_PATH, 'r+b') as f:
                    # Overwrite with random data
                    f.write(os.urandom(os.path.getsize(WALLET_FILE_PATH)))
                    # Overwrite with zeros
                    f.seek(0)
                    f.write(bytearray(b'\x00') * os.path.getsize(WALLET_FILE_PATH))
                    # Overwrite with ones
                    f.seek(0)
                    f.write(bytearray(b'\xFF') * os.path.getsize(WALLET_FILE_PATH))

            os.remove(WALLET_FILE_PATH)  # Remove file after overwrites
            logging.info("Wallet data destroyed securely.")
            print("Wallet data destroyed securely.")

        except Exception as e:
            logging.error(f"Error destroying wallet data: {e}")
            print("An error occurred while trying to destroy wallet data.")

    else:
        print("Wallet file does not exist.")

    # Option 2: Use a secure delete tool (if available)
    try:
        os.system(f"shred -u {WALLET_FILE_PATH}")  # Securely delete using shred
        logging.info("Wallet data securely deleted using shred.")
    except Exception as e:
        logging.error(f"Error using shred to delete wallet data: {e}")