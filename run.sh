#!/bin/bash

#install pip
echo "check and installing pip..."
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing pip..."
    sudo apt-get install -y python3-pip
else
    echo "pip already installed."
fi

## pip flask to run API
pip install requests flask

# Execute py script
python3 swapi.py &
sleep 5

echo "connecting URLs..."
for url in "http://127.0.0.1:5000/powerful_weapon" "http://127.0.0.1:5000/hottest_planets" "http://127.0.0.1:5000/appears_most" "http://127.0.0.1:5000/fastest_ships"
do
    echo "acessar: $url"
    curl -s $url
    echo ""
done

echo "O servidor está em execução."
