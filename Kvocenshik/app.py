from flask import Flask, redirect, request, jsonify, render_template, url_for
import folium
import math
import requests
import joblib

from haversine import haversine
from functions import *

app = Flask(__name__)

KREMLIN_LAT = 55.75141
KREMLIN_LON = 37.61896

@app.route('/', methods=['GET', 'POST'])
def route_price():
    if request.method == 'GET':
        return render_template('index.html', header='Оценщик квартир'), 200
    if request.method == 'POST':
        input_address = str(request.form['address'])
        input_metro = str(request.form['metro'])
        input_rooms = str(request.form['rooms'])
        input_square = float(request.form['square'])
        input_repair = str(request.form['type of repair'])
        input_ceiling_height = float(request.form['ceiling height'])
        input_house_type = str(request.form['house type'])
        input_parking = str(request.form['parking'])
        input_apartment_floor = int(request.form['apartment floor'])
        input_number_of_storeys_of_the_house = int(
            request.form['number of storeys of the house'])
        input_number_of_balconies = int(request.form['number of balconies'])
        input_number_of_loggias = int(request.form['number of loggias'])
        input_separate_bathroom = int(request.form['separate bathroom'])
        input_combined_bathroom = int(request.form['combined bathroom'])
        input_passenger_elevator = int(request.form['passenger elevator'])
        input_service_lift = int(request.form['service lift'])

        lat, lon, area_name, address_name = get_coords(input_address)
        distance = get_distance(lat, lon, KREMLIN_LAT, KREMLIN_LON)

        arr_features = [
          input_ceiling_height,
          input_number_of_balconies,
          input_number_of_loggias,
          input_passenger_elevator,
          input_service_lift,
          input_combined_bathroom,
          input_separate_bathroom,
          input_square,
          input_number_of_storeys_of_the_house,
          input_apartment_floor,
          lon,
          distance]

        arr_metro = get_metro(input_metro)
        arr_parking = get_parking(input_parking)
        arr_repair = get_repair(input_repair)
        arr_house_type = get_house_type(input_house_type)
        arr_circle = get_circle(distance)
        arr_rooms = get_rooms(input_rooms)
        arr_district = get_district(input_metro)
        arr_neighborhood = get_neighborhood(input_metro)

        arr_features += arr_metro 
        arr_features += arr_parking
        arr_features += arr_repair
        arr_features += arr_house_type
        arr_features += arr_circle
        arr_features += arr_rooms
        arr_features += arr_district
        arr_features += arr_neighborhood

        if area_name != 'Москва':
             not_moscow = 'Москва (а не %s!), ' %area_name
             return render_template('index.html', header='текс', not_mos=not_moscow), 200

        price = get_price(arr_features)
        
        return get_map(lat, lon, price, input_address, address_name)


@app.route('/')
def get_map(lat, lon, price, input_address, address_name):
    address = address_name
    loc = '<h3 style="line-height:50px; text-align:center; font-family: Marker Felt">Рыночная стоимость квартиры:<br></h3>' + '<h1 style="text-align:center; font-family: Marker Felt">' + price + ' руб.<br></h1>' + '<h4 style="text-align:center; font-family: Marker Felt; margin-top: 30px;">' + address + '<br></h4>' + '<div style="text-align: -webkit-center; margin-top:100px"><img style="width:300px; height:300px;" src="/static/img02.png"/></div>'
    price_html = '<div style="font-size:16px; width:34%; height:85%; float:left; box-shadow: 10px 0 10px 0 rgb(0 0 0 / 10%); background-color:rgb(244,244,244)"><b>{}</b></div>'.format(loc)   
    map = folium.Map(location=[lat, lon], zoom_start=16, tiles='OpenStreetMap', width='66%', height="85%")
    marker_cluster = MarkerCluster().add_to(map)
    folium.Marker(location=[lat, lon],
                  icon=folium.Icon(color='red')).add_to(marker_cluster)
    map.get_root().html.add_child(folium.Element(price_html))
    return  map._repr_html_(), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
