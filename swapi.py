from flask import Flask, jsonify
import requests
from collections import Counter

#FLASK to work with API
app = Flask(__name__)

#url base
url = 'https://swapi.dev/api/'

##trying connection
def get_data_from_api(endpoint):
    response = requests.get(f'{url}{endpoint}/')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Erro: {response.status_code}')
        return None

def get_all_data(endpoint):  ##method to get all the informations from API
    results = []
    endpoint_url = f'{url}{endpoint}/'
    while endpoint_url:
        response = requests.get(endpoint_url)
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

@app.route('/appears_most', methods=['GET']) #characters
def get_top_characters():
    film_characters = [person['name'] for film in films for person in film.get('characters', [])]
    count = Counter(film_characters)
    top_characters = count.most_common(5) ##the 5 characters that appear the most
    return jsonify(top_characters)

@app.route('/hottest_planets', methods=['GET'])
def get_hottest_planets():
    sorted_planets = sorted(planets, key=lambda x: x['climate'], reverse=True)
    hottest_planets = sorted_planets[:3] ##the 3 hottest planets, considering the climate field
    return jsonify(hottest_planets)

@app.route('/powerful_weapon', methods=['GET'])
def get_powerful_starships():
    sorted_starships = sorted(starships, key=lambda x: x['model'], reverse=True)
    powerful_starships = sorted_starships[:3] ##the 3 most powerful weapons following the model
    return jsonify(powerful_starships)


@app.route('/fastest_ships', methods=['GET'])
def get_fastest_ships():
    sorted_starships = sorted(starships, key=lambda x:  x['max_atmosphering_speed'], reverse=True)
    fastest_ships = sorted_starships[:3] ## the 3 fastest ships, considering the max_atmosphering_speed field
    return jsonify(fastest_ships)

if __name__ == '__main__':
    app.run(debug=True)
