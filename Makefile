PYTHON=python3.10

ENV_DIR=.env_$(PYTHON)
IN_ENV=. $(ENV_DIR)/bin/activate &&

env: $(ENV_DIR)

setup:
	$(PYTHON) -m venv $(ENV_DIR)
	$(IN_ENV) python -m pip install --upgrade pip
	$(IN_ENV) python -m pip install --upgrade -r requirements.txt

build:
	$(IN_ENV) python -m pip install --editable .

run:
	@ $(IN_ENV) git-vain
