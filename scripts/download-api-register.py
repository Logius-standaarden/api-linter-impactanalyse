import certifi
import os
import socket
import ssl
import urllib.request
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from os import path

IMPACT_ANALYSE_DIRECTORY = Path(__file__).parent.parent.resolve()
API_REGISTER_DIRECTORY = IMPACT_ANALYSE_DIRECTORY / "api-register"
API_DEFINITIONS_DIRECTORY = API_REGISTER_DIRECTORY / "definitions"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

request = urllib.request.Request(
    "https://gitlab.com/commonground/don/don-content/-/archive/main/don-content-main.zip?path=content/api"
)
with urllib.request.urlopen(request, timeout=20, context=SSL_CONTEXT) as http_request:
    zip_file = ZipFile(BytesIO(http_request.read()))

API_DEFINITIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)
for filename in os.listdir(API_DEFINITIONS_DIRECTORY):
    os.unlink(API_DEFINITIONS_DIRECTORY / filename)

for file in zip_file.namelist():
    if Path(file).suffix in [".yml", ".yaml"]:
        with zip_file.open(file) as yaml_file_in_zip:
            yaml_contents = yaml_file_in_zip.read().decode("utf-8")
            yaml_path = Path(file).stem + ".yaml"
            with open(API_DEFINITIONS_DIRECTORY / yaml_path, "w") as download_location:
                download_location.write(yaml_contents)
