import json
import uvicorn

from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from starlette.responses import Response

from models import Secret
from crypto import Crypto
from settings import DATABASE, PORT, LOG_LEVEL


app = FastAPI()
crypto = Crypto()
client = MongoClient(host=DATABASE['HOST'], port=DATABASE['PORT'])
database = client[DATABASE['NAME']]
collection = database[DATABASE['COLLECTION']]


@app.post('/generate', status_code=201)
async def generate(secret: Secret) -> Response:
    """The method receives a JSON with 'secret_text' and 'phrase' fields as input and returns the 'secret_key'

    JSON fields:
        secret_text: str
        phrase: str

    Request body example:
        {
            "secret_text": "string",
            "phrase": "string"
        }

    The function generates a secret key based on the input
    and returns it in JSON with the 'secret_key' field

    Successful response example:
        {
            "secret_key": "string"
        }

    All fields must be non null
    Strings can not be empty

    Validation error:
        {
            "detail": [
                {
                    "loc": [
                        "string"
                    ],
                    "msg": "string",
                    "type": "string"
                }
            ]
        }

    """
    crypto.encrypt_secret(secret)
    crypto.generate_secret_key(secret)

    collection.insert_one(secret.dict())

    res: str = json.dumps({
        'secret_key': secret.secret_key
    })

    return Response(status_code=201, content=res, media_type='application/json')


@app.get('/secrets/{secret_key}', status_code=200)
async def get_secret(secret_key: str, code_phrase: str = "") -> Response:
    """The method receives a code phrase as input and returns the secret

    :param code_phrase:
    :type code_phrase: str
    :return: decrypted secret or an error
    :rtype: JSON

    Not found error:
        {
            "detail": "The secret for this URL did not exist or was read"
        }

    If an invalid code phrase is specified
    HTTPException with status_code=401 is thrown

    Unauthorized error:
        {
            "detail" : "The code phrase is wrong"
        }

    """
    secret_dict: dict = collection.find_one({'secret_key': secret_key})

    if not secret_dict:
        raise HTTPException(status_code=404, detail="The secret for this URL did not exist or was read")

    secret: Secret = Secret(**secret_dict)
    crypto.decrypt_secret(secret)

    if not secret.phrase == code_phrase:
        raise HTTPException(status_code=403, detail="The code phrase is wrong")

    collection.delete_one({'secret_key': secret_key})

    res: str = json.dumps({
        'secret': secret.secret_text
    })

    return Response(content=res, media_type='application/json')


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
