from flask import Flask, jsonify
import requests
from collections import Counter

#FLASK to work with API
app = Flask(__name__)

#url base
url = 'https://swapi.dev/api/'

##trying connection
def get_data_from_api(endpoint):
    response = requests.get(f'{url}{endpoint}/', verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Erro: {response.status_code}')
        return None

def get_all_data(endpoint):  ##method to get all the informations from API
    results = []
    endpoint_url = f'{url}{endpoint}/'
    while endpoint_url:
        response = requests.get(endpoint_url, verify=False)
        if response.status_code == 200:
            data = response.json()
            results.extend(data['results'])
            endpoint_url = data.get('next')
        else:
            print(f'Erro ao acessar {endpoint_url}')
            endpoint_url = None
    return results

##loading the data
films = get_all_data('films')
people = get_all_data('people')
planets = get_all_data('planets')
starships = get_all_data('starships')
vehicles = get_all_data('vehicles')

@app.route('/films', methods=['GET']) ##get films
def get_films():
    return jsonify(films)

@app.route('/people', methods=['GET']) ##get people
def get_people():
    return jsonify(people)

@app.route('/planets', methods=['GET']) ##get planets
def get_planets():
    return jsonify(planets)

@app.route('/starships', methods=['GET']) ##get armas
def get_starships():
    return jsonify(starships)

@app.route('/vehicles', methods=['GET']) #veiculos
def get_vehicles():
    return jsonify(vehicles)


@app.route('/appears_most', methods=['GET'])
def get_top_characters():
    character_urls = []
    for film in films:
        characters = film.get('characters', [])
        if isinstance(characters, list):
            character_urls.extend(characters)
        else:
            print(f"Erro: 'characters' no filme '{film.get('title', 'Desconhecido')}' não é uma lista.")
    if not character_urls:
        return jsonify({"message": "Nenhum personagem encontrado"}), 404
    character_names = []
    for url in character_urls:
        character_id = url.split('/')[-2] 
        character_data = get_data_from_api(f'people/{character_id}')
        if character_data and 'name' in character_data:
            character_names.append(character_data['name'])
    count = Counter(character_names)
    top_characters = count.most_common(5) ##the 5 characters that appear the most
    top_characters_response = [{"name": name, "count": count} for name, count in top_characters] ##json form
    return jsonify(top_characters_response)


@app.route('/hottest_planets', methods=['GET'])
def get_hottest_planets():
    def climate_rank(climate):
        climate_order = {
            'hot': 4,
            'arid': 3,
            'temperate': 2,
            'cool': 1,
            'unknown': 0
        }
        return climate_order.get(climate.lower(), 0)  #unk is cold like 
    sorted_planets = sorted(planets, key=lambda x: climate_rank(x.get('climate', 'unknown')), reverse=True) 
    hottest_planets = sorted_planets[:3] ##the 3 hottest planets, considering the climate field
    hottest_planets_response = [{'name': planet['name'], 'climate': planet.get('climate', 'unknown')} for planet in hottest_planets]
    return jsonify(hottest_planets_response)


@app.route('/powerful_weapon', methods=['GET'])
def get_powerful_starships():
    sorted_starships = sorted(starships, key=lambda x: x.get('model', ''), reverse=True)
    powerful_starships = sorted_starships[:3]  ##the 3 most powerful weapons following the model
    powerful_starships_response = [{'name': starship['name'], 'model': starship.get('model', 'unknown')} for starship in powerful_starships]
    return jsonify(powerful_starships_response)


@app.route('/fastest_ships', methods=['GET'])
def get_fastest_ships():
    def parse_speed(speed):
        try:
            return int(speed.replace(',', ''))  
        except (ValueError, AttributeError):
            return 0 
    sorted_starships = sorted(starships, key=lambda x: parse_speed(x.get('max_atmosphering_speed', '0')), reverse=True)
    fastest_ships = sorted_starships[:3]  ## the 3 fastest ships, considering the max_atmosphering_speed field
    fastest_ships_response = [{'name': starship['name'], 'max_atmosphering_speed': starship.get('max_atmosphering_speed', 'unknown')} for starship in fastest_ships]
    return jsonify(fastest_ships_response)


if __name__ == '__main__':
    app.run(debug=True)
