import http.client
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config.config import Config

conn = http.client.HTTPSConnection("tennis-api-atp-wta-itf.p.rapidapi.com")

headers = {
    'x-rapidapi-key': Config.Api_keys.rapid_key,
    'x-rapidapi-host': "tennis-api-atp-wta-itf.p.rapidapi.com",
    'Content-Type': "application/json"
}

player_id = []
for player in range(5992, 5000, -1):
    conn.request("GET", f"/tennis/v2/atp/player/profile/{player}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))