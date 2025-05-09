Scripts om een impactanalyse te doen van spectral linter configuratie wijzigingen voor de API Design Rules.

Om te runnen, doe het volgende:

```sh
cd scripts/
./install-python-dependencies.sh
source ./venv/bin/activate

# Download de Zip van GitLab
python download-api-register.py
# Download the `openapi.json` files van de API's uit het register
python download-openapi-files.py
# Run de linter voor 1 specifieke regel, in dit geval "no-trailing-slash"
python run-spectral-for-single-rule.py --rule no-trailing-slash
```
