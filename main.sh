if [[ "$VIRTUAL_ENV" == "" ]]; then
	source .venv/bin/activate
fi
python src/main.py
python server.py --dir public
