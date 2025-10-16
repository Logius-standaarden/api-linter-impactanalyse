import json
import os
import statistics
from pathlib import Path

IMPACT_ANALYSE_DIRECTORY = Path(__file__).parent.parent.resolve()
API_REGISTER_DIRECTORY = IMPACT_ANALYSE_DIRECTORY / "api-register"
API_DEFINITIONS_DIRECTORY = API_REGISTER_DIRECTORY / "definitions"

def get_adr_score_for_api_definition(api_definition):
    with open(API_DEFINITIONS_DIRECTORY / api_definition) as definition_file:
        json_file = json.load(definition_file)
        return json_file["adrScore"]

api_definitions = [
    file
    for file in os.listdir(API_DEFINITIONS_DIRECTORY)
    if os.path.isfile(API_DEFINITIONS_DIRECTORY / file)
]

adr_scores = [
    adr_score
    for api_definition in api_definitions
    if (adr_score := get_adr_score_for_api_definition(api_definition))
    is not None
]

perfect_scores = len([adr_score for adr_score in adr_scores if adr_score == 100])
perfect_score_percentage = perfect_scores / len(adr_scores) * 100

above_80_scores = len([adr_score for adr_score in adr_scores if adr_score > 80])
above_80_score_percentage = above_80_scores / len(adr_scores) * 100

print(adr_scores)
print(f"Minimum score: {min(adr_scores)}")
print(f"Average score: {statistics.mean(adr_scores)}")
print(f"Perfect scores: {perfect_scores} ({perfect_score_percentage:.1f}%)")
print(f"Above 80 scores: {above_80_scores} ({above_80_score_percentage:.1f}%)")
