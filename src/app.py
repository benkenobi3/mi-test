import json
import uvicorn

from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from starlette.responses import Response

from models import Secret
from settings import DATABASE, PORT, LOG_LEVEL
from crypto import Crypto


app = FastAPI()
crypto = Crypto()
client = MongoClient(host=DATABASE['HOST'], port=DATABASE['PORT'])
database = client[DATABASE['NAME']]
collection = database[DATABASE['COLLECTION']]


@app.post('/generate')
async def generate(secret: Secret) -> Response:

    secret.validate_fields()

    crypto.encrypt_secret(secret)
    crypto.generate_secret_key(secret)

    collection.insert_one(secret.dict())

    res: str = json.dumps({
        'secret_key': secret.secret_key
    })

    return Response(content=res, media_type='application/json')


@app.get('/secrets/{secret_key}')
async def get_secret(secret_key: str, secret_phrase: str) -> Response:

    secret_dict: dict = collection.find_one({'secret_key': secret_key})

    if not secret_dict:
        raise HTTPException(status_code=404, detail="The secret for this URL did not exist or was read")

    secret: Secret = Secret(**secret_dict)
    crypto.decrypt_secret(secret)

    if not secret.phrase == secret_phrase:
        raise HTTPException(status_code=401, detail="The secret phrase is wrong")

    collection.delete_one({'secret_key': secret_key})

    res: str = json.dumps({
        'secret': secret.secret_text
    })

    return Response(content=res, media_type='application/json')


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
