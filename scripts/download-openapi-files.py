import certifi
import json
import os
import socket
import ssl
import urllib.request
import yaml
from pathlib import Path

IMPACT_ANALYSE_DIRECTORY = Path(__file__).parent.parent.resolve()
API_REGISTER_DIRECTORY = IMPACT_ANALYSE_DIRECTORY / "api-register"
API_DEFINITIONS_DIRECTORY = API_REGISTER_DIRECTORY / "definitions"
OPEN_API_CACHE_DIRECTORY = API_REGISTER_DIRECTORY / "open-api-specs"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def get_specification_url_for_api_definition(api_definition):
    with open(API_DEFINITIONS_DIRECTORY / api_definition) as yaml_file:
        try:
            yaml_object = yaml.safe_load(yaml_file)
            environments = yaml_object.get("environments", [])

            for environment in environments:
                if environment["name"] == "production":
                    return environment.get("specification_url", None)

            return None
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


api_definitions = [
    file
    for file in os.listdir(API_DEFINITIONS_DIRECTORY)
    if os.path.isfile(API_DEFINITIONS_DIRECTORY / file)
]
specification_urls = [
    (api_definition, specification_url)
    for api_definition in api_definitions
    if (specification_url := get_specification_url_for_api_definition(api_definition))
    is not None
]

OPEN_API_CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
for filename in os.listdir(OPEN_API_CACHE_DIRECTORY):
    os.unlink(OPEN_API_CACHE_DIRECTORY / filename)

total_downloaded = 0
total_invalid_json = 0
total_http_error = 0
total_certificate_error = 0
total_timeout_error = 0

for api_definition, specification_url in specification_urls:
    print(f"Downloading {specification_url} for {api_definition}")
    try:
        request = urllib.request.Request(specification_url)
        request.add_header("Accept", "application/json")
        with urllib.request.urlopen(
            request, timeout=3, context=SSL_CONTEXT
        ) as http_request:
            download_path = Path(api_definition).stem + ".json"
            maybe_json_format = http_request.read().decode("utf-8")
            try:
                # Check if it is actually JSON or a different format (in which case we don't write)
                # the file
                json_object = json.loads(maybe_json_format)
                with open(
                    OPEN_API_CACHE_DIRECTORY / download_path, "w"
                ) as download_location:
                    download_location.write(json.dumps(json_object, indent=2))
                    total_downloaded += 1
            except json.decoder.JSONDecodeError as json_error:
                print(
                    f"Skipped downloading {specification_url} because of {json_error}"
                )
                total_invalid_json += 1
    except urllib.error.HTTPError as http_error:
        print(f"Skipped downloading {specification_url} because of {http_error}")
        total_http_error += 1
    except urllib.error.URLError as certificate_error:
        print(f"Skipped downloading {specification_url} because of {certificate_error}")
        total_certificate_error += 1
    except socket.timeout as timeout:
        print(f"Timed out while loading {specification_url}")
        total_timeout_error += 1

print(f"""
Statistics:

Downloaded: {total_downloaded}
No JSON: {total_invalid_json}
Http issues: {total_http_error}
Certificate issues: {total_certificate_error}
Timeout issues: {total_timeout_error}
""")
