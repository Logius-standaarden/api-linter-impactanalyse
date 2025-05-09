import argparse
import os
import subprocess
import sys
import yaml
from pathlib import Path

IMPACT_ANALYSE_DIRECTORY = Path(__file__).parent.parent.resolve()
OPEN_API_CACHE_DIRECTORY = IMPACT_ANALYSE_DIRECTORY / "api-register" / "open-api-specs"
SPECTRAL_LINTER_LOCATION = (
    IMPACT_ANALYSE_DIRECTORY.parent / "API-Design-Rules" / "linter" / "spectral.yml"
)
GENERATED_LINTER_LOCATION = (
    IMPACT_ANALYSE_DIRECTORY / "api-register" / ".generated-spectral.yml"
)

SPECTRAL_NO_ERROR_FOUND_MESSAGE = "No results with a severity of 'error' found!\n"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--rule")
script_arguments = arg_parser.parse_args()

rule_to_run = script_arguments.rule

with open(SPECTRAL_LINTER_LOCATION) as linter_yaml:
    linter_rules = yaml.safe_load(linter_yaml)["rules"]
    if rule_to_run is None or rule_to_run not in linter_rules:
        print(
            f"""
Did not specify a valid rule: "{rule_to_run}". Choose one of the following:

%s
"""
            % "\n".join(linter_rules)
        )
        sys.exit(1)

    for rule in linter_rules:
        if rule == rule_to_run:
            yaml_rule = linter_rules[rule]

with open(GENERATED_LINTER_LOCATION, "w") as generated_linter:
    generated_yaml = dict(rules=dict())
    generated_yaml["rules"][rule_to_run] = yaml_rule
    yaml.dump(generated_yaml, generated_linter, default_flow_style=False)

total_specifications = 0
total_passing = 0
total_timed_out = 0

for open_api_spec in os.listdir(OPEN_API_CACHE_DIRECTORY):
    total_specifications += 1
    try:
        spectral_output = subprocess.run(
            [
                "spectral",
                "lint",
                "-r",
                GENERATED_LINTER_LOCATION,
                OPEN_API_CACHE_DIRECTORY / open_api_spec,
            ],
            timeout=10,
            check=False,
            stdout=subprocess.PIPE,
        )
        spectral_output = spectral_output.stdout.decode("utf-8")
        if spectral_output == SPECTRAL_NO_ERROR_FOUND_MESSAGE:
            total_passing += 1
        else:
            print(spectral_output)
    except subprocess.TimeoutExpired as timeout_error:
        total_timed_out += 1
        print(f"Timed out on {OPEN_API_CACHE_DIRECTORY / open_api_spec}")

print(f"""
Statistics for rule {rule_to_run}:

Analyzed: {total_specifications}
Passing: {total_passing}
Percentage: {int(total_passing / total_specifications * 100)}%

Timed out: {total_timed_out}
""")
