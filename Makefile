venv-python:
	virtualenv -p /usr/bin/python3 venv

venv-dev: venv-python
	./venv/bin/pip install -r dev-requirements.txt

venv-dev-upgrade:
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install --upgrade -r dev-requirements.txt

venv: venv-dev
	./venv/bin/pip install -r requirements.txt

venv-upgrade:
	./venv/bin/pip install --upgrade -r dev-requirements.txt
	./venv/bin/pip install --upgrade -r requirements.txt

format-asynio:
	./venv/bin/python -m black ./asyncio

run-asyncio:
	./venv/bin/python ./asyncio/main.py

run-sensor:
	./venv/bin/python ./sensor/test_sensor.py

run-textual:
	./venv/bin/python ./textual/main.py
