import os


# Uvicorn settings
# Uvicorn https://www.uvicorn.org/

PORT: int = int(os.environ.get('PORT', '80'))

LOG_LEVEL: str = 'debug'


# Database
# MongoDB https://www.mongodb.com/

DATABASE = {
    'NAME': os.environ.get('DB_NAME', 'SeriesDB'),
    'HOST': os.environ.get('DB_HOST', 'localhost'),
    'PORT': int(os.environ.get('DB_PORT', '27017')),
    'COLLECTION': 'secrets'
}
