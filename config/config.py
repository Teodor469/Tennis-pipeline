import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    
    class Api_keys:
        rapid_key = os.getenv("RAPID_API_KEY")