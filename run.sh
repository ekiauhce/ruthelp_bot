. env/bin/activate || exit

# Change us!
export TG_API_TOKEN=
export HOST_IP=

cd ./src/ || exit
python init_db.py && python main.py
cd ..

unset TG_API_TOKEN
unset HOST_IP

deactivate