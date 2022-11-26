import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", 'antony-tax-entity.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get("API_AUDIENCE",'TaxEntity')

## AuthError Exception
'''
AuthError Exception
A class for errors that will be raised
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
This method will attempt to get the header from the request
it will raise an AuthError if no header is present
it will attempt to split bearer and the token
it will raise an AuthError if the header is malformed
return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({'code':'Authorization header missing','description':'Authorization header is expected'},401)

    auth_parts = auth_header.split(" ")
    if auth_parts[0].lower()!='bearer':
        raise AuthError({'code':'Invalid header','description':'Authorization header must start with "Bear"'},401)
    elif len(auth_parts)==1:
        raise AuthError({'code':'Invalid header','description':'Token malformed'},401)
    elif len(auth_parts)>2:
        raise AuthError({'code':'Invalid header','description':'Authorization header must be bearer token'},401)
    token = auth_parts[1]
    
    return token

        

'''
The function takes a permission and a payload like below
permission: string permission (i.e. 'post:accountnat')
payload: decoded jwt payload
it will raise an AuthError if permissions are not included in the payload
it will raise an AuthError if the requested permission string is not in the payload permissions array
return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({'code':'Invalid header','description':'permissions not found'},401)
    if permission not in payload['permissions']:
        raise AuthError({'code':'Invalid header','description':'forbidden from resource'},403)
    return True

'''
The function takes a json web token (which is a string) as input
For it to be valid it should be an Auth0 token with key id (kid)
The token wil be verified using Auth0 /.well-known/jwks.json
A payload should be decoded the token
It will validate the claims and return the decoded payload
'''
def verify_decode_jwt(token):
    url_raw = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    json_raw = json.loads(url_raw.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    #check for availability of kid
    if 'kid' not in unverified_header:
        raise AuthError({'code':'invalid_header','description':'Authorization malformed'},401)
    for key in json_raw['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
        if rsa_key:
            try:
                payload = jwt.decode(token,rsa_key, algorithms=ALGORITHMS,audience=API_AUDIENCE,issuer='https://' + AUTH0_DOMAIN + '/')
                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError({'code':'token expired','description':'Token expired'},401)
            except jwt.JWTClaimsError:
                raise AuthError({'code':'invalid_claims','description':'Incorrect claims'},401)
            except Exception:
                raise AuthError({'code':'invalid_header','description':'Unable to parse token'},400)
    raise AuthError({'code':'invalid_header','description':'correct key not found'},400)

'''
The function takes permission: string permission (like 'post:accountant')
it Will use the get_token_auth_header method to get the token
it will use the verify_decode_jwt method to decode the jwt
it will use the check_permissions method validate claims and check the requested permission
return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return func(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator