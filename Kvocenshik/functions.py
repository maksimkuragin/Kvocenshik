import folium
import math
import requests
import numpy as np
import joblib
import xgboost as xgb
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dicts import *
from arrs import *


xgb = joblib.load('model03.joblib')
sc=joblib.load('std_scaler.bin')

YANDEX = 'NUMBER API'

def get_distance(lat, lon, KREMLIN_LAT, KREMLIN_LON):
    return round(geodesic((lat, lon), (KREMLIN_LAT, KREMLIN_LON)).km, 2)

def get_metro(input_metro):
  arr_metro = [0] * len(metro_dict)
  index = metro_dict[input_metro]
  arr_metro[index] = 1
  return arr_metro 

def get_parking(input_parking):
  arr_parking = [0] * len(parking_dict)
  index = parking_dict[input_parking]
  arr_parking[index] = 1
  return arr_parking 

def get_repair(input_type_of_repair):
  arr_repair = [0] * len(repair_dict)
  index = repair_dict[input_type_of_repair]
  arr_repair[index] = 1
  return arr_repair 

def get_house_type(input_house_type):
  arr_house_type = [0] * len(house_type_dict)
  index = house_type_dict[input_house_type]
  arr_house_type[index] = 1
  return arr_house_type
  
def get_circle(distance):
  res = ''
  if distance < 2.5:
    res = 'Садовое кольцо'
  elif 2.5 < distance < 5:
    res = 'ТТК'
  elif 5 < distance < 17:
    res = 'МКАД'
  else:
    res = 'ЗАМКАДЫШИ'
  res
  arr_circle = [0] * len(circle_dict)
  index = circle_dict[res]
  arr_circle[index] = 1
  return arr_circle

def get_rooms(input_rooms):
  arr_rooms = [0] * len(rooms_dict)
  index = rooms_dict[input_rooms]
  arr_rooms[index] = 1
  return arr_rooms

def get_district(input_metro):
  res = ''
  if input_metro in VAO:
    res = 'ВАО'
  elif input_metro in ZAO:
    res = 'ЗАО'
  elif input_metro in NAO:
    res = 'НАО'
  elif input_metro in SAO:
    res = 'САО'
  elif input_metro in SVAO:
    res = 'СВАО'
  elif input_metro in SZAO:
    res = 'СЗАО'
  elif input_metro in CAO:
    res = 'ЦАО'
  elif input_metro in UVAO:
    res = 'ЮВАО'
  elif input_metro in UAO:
    res = 'ЮАО'
  elif input_metro in UZAO:
    res = 'ЮЗАО'
  arr_district = [0] * len(district_dict)
  index = district_dict[res]
  arr_district[index] = 1
  return arr_district

def get_neighborhood(input_metro):
  res = ''
  for key, val in my_dict.items():
    if input_metro in val:
      res = key
  arr_neighborhood = [0] * len(neighborhood_dict)
  index = neighborhood_dict[res]
  arr_neighborhood[index] = 1
  return arr_neighborhood

def get_price(arr_features):
  norm_x = sc.transform(np.array(arr_features).reshape(1, -1))
  cost = xgb.predict(norm_x)
  str_cost = str(int(cost[0]))
  return f'{str_cost[:-6]} {str_cost[-6:-3]} {str_cost[-3:]}'

def get_coords(input_address):
  geodata = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX}&geocode={input_address}&format=json').json()
  lon, lat = geodata['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
  area_name = geodata['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'].get('metaDataProperty'
  ).get('GeocoderMetaData').get('AddressDetails').get('Country').get('AdministrativeArea').get('AdministrativeAreaName')
  address_name = geodata['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'].get('metaDataProperty'
  ).get('GeocoderMetaData').get('AddressDetails').get('Country').get('AddressLine')
  return float(lat), float(lon), area_name, address_name
