import jwt
from datetime import datetime

def decode_jwt(token):
    try:
        # Decode without verification for inspection
        decoded_payload = jwt.decode(token, options={"verify_signature": False})
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")