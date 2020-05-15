import os
import json

import uvicorn
from pymongo import MongoClient
from xxhash import xxh64

from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from starlette.responses import Response

DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
DB_NAME: str = os.environ.get('DB_NAME', 'SeriesDB')
DB_PORT: int = int(os.environ.get('DB_PORT', '27017'))

app = FastAPI()

client = MongoClient(host=DB_HOST, port=DB_PORT)
db = client[DB_NAME]
db_collection = db['secrets']


class Secret(BaseModel):
    secret_text: str
    phrase: str
    secret_key: str = None


class SecretPhrase(BaseModel):
    phrase: str


@app.post('/generate')
async def generate(secret: Secret) -> Response:
    validate_secret(secret)
    secret.secret_key = xxh64(secret.secret_text + secret.phrase).hexdigest()[:7]

    insert_secret(db_collection, secret.dict())

    res: str = json.dumps({
        'secret_key': secret.secret_key
    })

    return Response(content=res, media_type='application/json')


@app.post('/secrets/{secret_key}')
async def get_secret(secret_key: str, secret_phrase: SecretPhrase) -> Response:
    secret: dict = find_secret(db_collection, {'secret_key': secret_key})

    if not secret:
        raise HTTPException(status_code=404, detail="The secret for this URL did not exist or was read")

    if not secret['phrase'] == secret_phrase.phrase:
        raise HTTPException(status_code=401, detail="The secret phrase is wrong")

    delete_secret(db_collection, secret)

    res: str = json.dumps({
        'secret': secret['secret_text']
    })

    return Response(content=res, media_type='application/json')


def validate_secret(secret: Secret):
    if (not secret.secret_text) | (not secret.phrase):
        raise HTTPException(status_code=400, detail="Fields can not be empty")


def insert_secret(collection, secret_dict: dict):
    collection.insert_one(secret_dict)


def delete_secret(collection, secret_dict: dict):
    collection.delete_one(secret_dict)


def find_secret(collection, secret_dict: dict):
    return collection.find_one(secret_dict)


if __name__ == "__main__":
    PORT: int = int(os.environ.get('PORT', '80'))
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level="debug")
