# Test task in the Market Intelligence unit
Task: you need to make an HTTP service for one-time secrets


## Quick start
    $ docker-compose up
    
## API methods
  ### /generate
  The method receives a JSON with 'secret_text' and 'phrase' fields as input and returns the 'secret_key'
  
  #### Request body example:
    {
      "secret_text": "string",
      "phrase": "string"
    }
    
 #### Successful response example:
    {
      "secret_key": "string"
    }
    
 #### Validation error:
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
    
 ### /secrets/{secret_key}
 The method receives a code phrase as input and returns the secret

 #### Example:
    /secrets/secretkey?code_phrase=string

 #### Not found error:
    {
      "detail": "The secret for this URL did not exist or was read"
    }

 #### Unauthorized error:
    {
      "detail" : "The code phrase is wrong"
    }
    
## Testing
    pip install -r requirements.txt
    cd src
    python tests.py
