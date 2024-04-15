# JWT AUTH API

This API validates the JWT (JSON Web Token) that is passed to the endpoint in the Authorization headers and responds with a JSON containing information whether the JWT is valid or not. If the JWT is invalid, a reason is included in the response.

## Requirements
- Python 3.10.12 or higher

## How to use the API
- Install dependencies with ```pip install -r requirements.txt```

- Run the server with ```python3 src/main.py```

- The server is now operating at http://localhost:8000/

- The only endpoint is http://localhost:8000/auth

- Create a JWT with following specs:
    - JWT Header must contain the following fields:
        - "typ": "JWT"
        - "alg": "RS256" 
        - "x5u":  URL of the PEM-encoded X.509 certificate
    - JWT payload must contain the following fields:
        - "iat": timestamp when the token is being created.
        - "exp": timestamp when the token expires

- Send a GET request to http://localhost:8000/auth with the JWT in the Authorization header.

- Example request can look like this:
```
GET http://localhost:8000/auth HTTP/1.1
Host: localhost
Accept: application/json
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dSI6Imh0dHA6Ly9sb2NhbGhvc3Q6MzAwMC9wdWJrZXkucGVtIn0.eyJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTUxNjI0MzAyMn0.hpBj2icrcN2onx5vifXluSAOavEn3UhtO7zUTRIpZZU1_JxNFp7VpH6RuTXqMPN_vjc7O9d5Lvlh_uNp2lRRJfbuprSF35VTe6ivbDLK9xCboJ1VTsJ1mPHFwHIbSGDHis_ytCi5s_Lgs7o4wBnQq4UO5DejL-GyHQZmLLtBRGZcar7tcF83hdEdIbDuCVrFJ8iG-LoyQ6Bodos5GndWYX75J0mrAGKb-5PmqGycafuXMO-R-37nkC0BJs_-MS_djTlAOZcdbLKNr-8tE8iMhL1kYjo23tP3JTgtsseAlLgWj71ITc3Py6c0haucjuC5iKfMYxeJq58yPn413XNdmw
```

- The server responds ``` { "valid": true } ``` is the JWT is valid.

- The server responds with an error and explanation if the JWT is invalid.

### Possible HTTP response codes and explanations

- 200: The request was successful and the JWT provided is valid
- 400: There was a problem in the request format (i.e. missing header)
- 422: The request was formed correctly but the JWT token was invalid due to an error (i.e. Token expired) or could not be verified (i.e. invalid x5u)


### Creating a valid RS256 JWT token and serving the public key locally for demonstrative purposes and integration testing

- Navigate to backend_for_testing directory

- Create a private key and corresponding public key pair with

    - ```openssl genrsa -out test_private_key.pem 4096```

    - ```openssl rsa -in test_private_key.pem -pubout -outform PEM -out test_public_key.pem```

- Generate an encoded JWT token with ```python3 jwt_generator.py```

- Copy the encoded JWT token from the terminal

- Start the dummy backend server with ```python3 dummy_backend.py```

    - The server is now sharing your "test_public_key.pem" at http://localhost:3000/pubkey.pem for validating the JWT token created earlier.

- Start the JWT Auth API with ``` python3 src/main.py ``` in the root directory

- Create a GET request with the encoded JWT token copied earlier:
```
GET http://localhost:8000/auth HTTP/1.1
Host: localhost
Accept: application/json
Authorization: Bearer { your encoded JWT }
```
- Here is a valid GET request created with [Postman](https://www.postman.com/):

    - ![Postman GET Request example](https://github.com/evahteri/jwt_auth_api/blob/main/documentation/example_request_postman.png)

- Here is a valid GET request created with curl:
    - ```curl -i --header "Authorization: Bearer { your encoded JWT }" http://localhost:8000/auth```

## Configuration
Maximum time to live for the token can be adjusted in the [configuration.py](src/configuration.py) file.

## Testing
Integration tests use the provided dummy backend for token validation.

- Start the dummy backend server with ```python3 src/backend_for_testing/dummy_backend.py```

- Run the tests with ```pytest```

## Flowgraph
![Flowgraph](https://github.com/evahteri/jwt_auth_api/blob/main/documentation/flowgraph.png)

## Usage Examples

### Incorrect headers

- Client:

```
GET http://localhost:8000/auth HTTP/1.1
Host: localhost
Accept: application/json
Authorization: Bearer { jwt with a RS512 alg header }
```

- JWT Auth Api:
```
HTTP/1.1 400 Bad Request
date: Mon, 15 Apr 2024 13:31:37 GMT
server: uvicorn
content-length: 88
content-type: application/json
Connection: close

{
  "detail": "Invalid algorithm. Alg header is RS512. The API is configured to use RS256."
}
```
### Valid JWT Token

- Client:
```
GET http://localhost:8000/auth HTTP/1.1
Host: localhost
Accept: application/json
Authorization: Bearer { valid jwt }
```
- JWT Auth API:
```
HTTP/1.1 200 OK
date: Mon, 15 Apr 2024 13:33:46 GMT
server: uvicorn
content-length: 14
content-type: application/json
Connection: close

{
  "valid": true
}
```
### Invalid JWT (signature validation fails due to error in x5u)

- Client:

```
GET http://localhost:8000/auth HTTP/1.1
Host: localhost
Accept: application/json
Authorization: Bearer { invalid jwt }
```


- JWT Auth API:
```
HTTP/1.1 422 Unprocessable Entity
date: Mon, 15 Apr 2024 13:36:52 GMT
server: uvicorn
content-length: 123
content-type: application/json
Connection: close

{
  "detail": "Invalid x5u. The certificate could not be retrieved. The url provided in x5u responded with a 404 status code."
}
```

## Documentation
- [Backlog](documentation/backlog.md)