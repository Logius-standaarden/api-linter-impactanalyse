import json
import os
import requests
import sys
import urllib
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
# Pages are one-indexed in the register
page = 1
# This is a dummy value to ensure we run the loop at least once. After the
# first request, this set to the correct amount
total_pages = 2
apis_in_api_register = []
# This is a dummy value. After the first request, this set to the correct amount
total_apis = -1
while page < total_pages + 1:
    try:
        apis_in_page = requests.get(API_REGISTER_API_ENDPOINT, verify=False, headers=API_REGISTER_HEADERS, params={'perPage': '50', 'page': page})
        page += 1
        apis = apis_in_page.json()
        apis_in_api_register.extend(apis)
        total_pages = int(apis_in_page.headers["total-pages"])
        total_apis = int(apis_in_page.headers["total-count"])
    except urllib.error.HTTPError as http_error:
        break

if len(apis_in_api_register) != total_apis:
    print(f"Invalid number of api's retrieved. Register reported {total_apis}, but retrieved {len(apis_in_api_register)}")
    sys.exit(1)

API_DEFINITIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)
for filename in os.listdir(API_DEFINITIONS_DIRECTORY):
    os.unlink(API_DEFINITIONS_DIRECTORY / filename)

for api in apis_in_api_register:
    with open(API_DEFINITIONS_DIRECTORY / api["id"], "w") as download_location:
        json.dump(api, download_location, indent=2)
