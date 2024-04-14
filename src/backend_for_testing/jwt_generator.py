import jwt
import os
from datetime import datetime

class JWTGenerator:
    def __init__(self):
        file_path_private_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_private_key.pem")
        with open(file_path_private_key, "r") as f:
            self.private_key = f.read()
        
        file_path_public_key = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_public_key.pem")
        with open(file_path_public_key, "r") as f:
            self.public_key_key = f.read()

        # keys can be generated with 
        # openssl genrsa -out test_private_key.pem 4096
        # openssl rsa -in test_private_key.pem -pubout -outform PEM -out test_public_key.pem
    
    
    def generate_jwt_token(self, iat: int, exp: int, typ: str = None, alg: str = None, x5u: str = None) -> str:
        """Generates a valid jwt token. Use x5u: "http://localhost:3000/pubkey.pem" to use
        the endpoint that the dummy_backend.py offers for validation.
        """
        payload = {
            "iat": iat,
            "exp": exp
        }

        headers = {}
        if x5u:
            headers["x5u"] = x5u
        if alg:
            headers["typ"] = typ
        if alg:
            headers["alg"] = alg
    
        encoded = jwt.encode(payload=payload, key=self.private_key, algorithm="RS256", headers=headers)

        return encoded

if __name__ == "__main__":
    iat = int(datetime.now().timestamp())
    print(JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256"))