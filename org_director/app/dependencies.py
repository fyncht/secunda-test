from fastapi import Header, HTTPException

API_KEY = "SECRETLOVELYAPIKEY"


def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
