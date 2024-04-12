import jwt
from datetime import datetime

class JWTGenerator:
    def __init__(self):
        self.private_key = open('test_private_key.pem', 'r').read()
        self.public_key = open('test_public_key.pem', 'r').read()
        # keys can be generated with 
        # openssl genrsa -out test_private_key.pem 4096
        # openssl rsa -in test_private_key.pem -pubout -outform PEM -out test_public_key.pem
    
    
    def generate_jwt_token(self):
        """Generates a valid jwt token. The x5u header is set to "http://localhost:3000/pubkey.pem",
        an endpoint that the dummy_backend.py offers for validation.
        Copy the jwt from "encoded starts" to "encoded ends" to the Authorization header to form a valid GET request.
        """
        iat = int(datetime.now().timestamp())

        payload = {
        "iss": "example.com",
        "iat": iat,
        "exp": iat + 5000
        }

        print("encoded starts")
        encoded = jwt.encode(payload=payload, key=self.private_key, algorithm="RS256", headers={"x5u": "http://localhost:3000/pubkey.pem", "typ": "JWT", "alg": "RS256"})

        print(encoded)

        print("encoded ends")

        decoded = jwt.decode(jwt=encoded, key=self.public_key, algorithms=["RS256"])

        print(decoded)

if __name__ == "__main__":
    JWTGenerator().generate_jwt_token()