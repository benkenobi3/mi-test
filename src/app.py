import json
from xxhash import xxh64

from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from pydantic import BaseModel


app = FastAPI()

data = {}


class Secret(BaseModel):
  secret_text: str
  phrase: str


class SecretPhrase(BaseModel):
  phrase: str


@app.post('/generate')
async def generate(secret: Secret) -> str:

  validate_secret(secret)
  secret_key: str = xxh64(secret.secret_text + secret.phrase).hexdigest()[:7]
  data[secret_key] = secret.dict()

  res: str = json.dumps({
    'secret_key' : secret_key
  })

  return Response(content=res, media_type='application/json')


@app.post('/secrets/{secret_key}')
async def get_secret(secret_key: str, secret_phrase: SecretPhrase):

  secret: str = data.get(secret_key) 

  if not secret:
    raise HTTPException(status_code=404, detail="The secret for this URL did not exist or was read")

  if not secret['phrase'] == secret_phrase.phrase:
    raise HTTPException(status_code=401, detail="The secret phrase is wrong")

  res: str = json.dumps({
    'secret' : secret['secret_text']
  })

  return Response(content=res, media_type='application/json')


def validate_secret(secret: Secret):
  if (not secret.secret_text) | (not secret.phrase):
    raise HTTPException(status_code=400, detail="Fields can not be empty")
