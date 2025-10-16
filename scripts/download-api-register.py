import json
import os
import requests
import sys
from pathlib import Path
from os import path

if 'API_KEY' not in os.environ:
    print("Did not specify API_KEY environment variable")
    sys.exit(1)

IMPACT_ANALYSE_DIRECTORY = Path(__file__).parent.parent.resolve()
API_REGISTER_DIRECTORY = IMPACT_ANALYSE_DIRECTORY / "api-register"
API_DEFINITIONS_DIRECTORY = API_REGISTER_DIRECTORY / "definitions"

API_REGISTER_API_ENDPOINT = "https://api.don.apps.digilab.network/api-register/v1/apis"
API_REGISTER_HEADERS = {'x-api-key': os.environ['API_KEY']}
page = 0
apis_in_api_register = []
while True:
    try:
        apis_in_page = requests.get(API_REGISTER_API_ENDPOINT, verify=False, headers=API_REGISTER_HEADERS, params={'perPage': '50', 'page': page})
        page += 1
        apis = apis_in_page.json()
        if len(apis) == 0:
            break
        apis_in_api_register.extend(apis)
    except urllib.error.HTTPError as http_error:
        break

API_DEFINITIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)
for filename in os.listdir(API_DEFINITIONS_DIRECTORY):
    os.unlink(API_DEFINITIONS_DIRECTORY / filename)

for api in apis_in_api_register:
    with open(API_DEFINITIONS_DIRECTORY / api["id"], "w") as download_location:
        json.dump(api, download_location, indent=2)
