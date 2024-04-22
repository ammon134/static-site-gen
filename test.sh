if [[ "$VIRTUAL_ENV" == "" ]]; then
	source .venv/bin/activate
fi
python -m unittest discover -s src
