. env/bin/activate || exit

cd ./src/ || exit
python init_db.py && python main.py
cd ..

deactivate