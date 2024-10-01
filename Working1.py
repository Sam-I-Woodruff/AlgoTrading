
from dotenv import load_dotenv
import os
import requests
import json
import time
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv('API_KEY')