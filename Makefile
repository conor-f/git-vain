PYTHON=python3.10

ENV_DIR=.env_$(PYTHON)
IN_ENV=. $(ENV_DIR)/bin/activate &&

env: $(ENV_DIR)

setup:
	$(PYTHON) -m venv $(ENV_DIR)
	$(IN_ENV) python -m pip install --upgrade pip

requirements:
	$(IN_ENV) python -m pip install --upgrade -r requirements.txt

build: requirements
	$(IN_ENV) python -m pip install --editable .

run:
	@ $(IN_ENV) git-vain

test_requirements:
	$(IN_ENV) python -m pip install --upgrade -r test_requirements.txt

star_repo:
	$(IN_ENV) star-repo --star conor-f/spotibar

unstar_repo:
	$(IN_ENV) star-repo --unstar conor-f/spotibar
