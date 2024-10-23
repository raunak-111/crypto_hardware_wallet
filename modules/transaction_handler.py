from ecdsa import SigningKey, SECP256k1

def sign_transaction(private_key_hex, transaction_data):
    signing_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    signature = signing_key.sign(transaction_data.encode())
    return signature
