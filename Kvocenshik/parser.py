import os
import logging
import requests
from selenium import webdriver
from stations import stations
import time

n_komnat = [1, 2, 3, 4, 5, 6, 7, 9]

def main():
    driver = webdriver.Chrome("/home/ni/Best_project/my_cian_parser/chromedriver.exe")
    for a in n_komnat:
        for i in range(1, 441):
            driver.get(f"https://www.cian.ru/export/xls/offers/?deal_type=sale&engine_version=2&foot_min=45&metro[0]={i}&object_type[0]=1&offer_type=flat&only_foot=2&room{a}=1")
            time.sleep(2)

if __name__ == "__main__":
    main()
