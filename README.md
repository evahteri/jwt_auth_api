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

## Configuration
Maximum time to live for the token can be adjusted in the [configuration.py](src/configuration.py) file.

## Testing
Automated unit tests can be run with command ```pytest```

## Documentation
- [Backlog](documentation/backlog.md)