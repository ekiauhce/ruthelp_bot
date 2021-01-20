. env/bin/activate

# Change us!
export TG_API_TOKEN=
export HOST_IP=

cd ./src/ || exit
python init_db.py || exit
python main.py

unset TG_API_TOKEN

deactivate