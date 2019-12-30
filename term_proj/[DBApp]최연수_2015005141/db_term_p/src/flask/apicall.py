import json
import requests
from pprint import pprint


def hosp_list(lat=37.5585146, lng=127.0331892):
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,
      'numOfRows': 9999,
      'ServiceKey': default_key,
      'yPos': lat,
      'xPos': lng,
      'radius': 5000,
      '_type': 'json'
    }
    r = requests.get(url, params=params)
    return r.json()


def pharm_list(lat=37.5585146, lng=127.0331892):
    url = "http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,
      'numOfRows': 9999,
      'ServiceKey': default_key,
      'yPos': lat,
      'xPos': lng,
      'radius': 5000,
      '_type': 'json'
    }
    r = requests.get(url, params=params)
    return r.json()


def test_run():
    clinics = hosp_list()
    pprint(clinics['response']['body']['items']['item'])
    pprint(pharm_list())



if __name__ == ("__main__"):
    test_run()