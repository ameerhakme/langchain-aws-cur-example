
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # OpenAI APIkey 
    API_KEYS_SECRET_NAME = "<YOUR OPENAI API KEY>"

    #OpenAI Model Name 
    MODEL_NAME="text-davinci-003"

    # S3 Bucket Name to store Cost Report
    BUCKET_NAME = "<YOUR S3 BUCKET WHERE YOU HAVE THE CUR FILE STORED>"
    KEY = "<CUR_FILE_Name.csv>"

config = Config()