from actions import *
from ts import *

import time
import datetime
import requests

REQUETE = "sail"
MAIL = "andreojules@gmail.com"
MDP = "cukqep-fipju8-puwcyR"

def auth(mail, mdp):
    try:
        payload_auth = {
            "@class": "AuthenticationRequest",
            "userName":mail,
            "password":mdp
        }
        resp = requests.post(hd.url_auth, headers=hd.headers_auth, json=payload_auth)
        data = resp.json()
        auth_token = data["authToken"]
        userId = data["userId"]
        return auth_token, userId
    except Exception as e:
        print("Erreur :", e)


url_auth = "https://prod.vro.sparks.virtualregatta.com/rs/device/Xcl3WbCUmfcu5pWCktUoC0slGT4xkbEt/AuthenticationRequest"
headers_auth = {
    "accept": "application/json",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://play.offshore.virtualregatta.com",
    "priority": "u=1, i",
    "referer": "https://play.offshore.virtualregatta.com/",
    "sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "x-platform": "WebGLPlayer",
    "x-version": "7.0.9"
}

url_heading = "https://prod.vro.sparks.virtualregatta.com/rs/device/Xcl3WbCUmfcu5pWCktUoC0slGT4xkbEt/LogEventRequest"
headers_heading = {
    "accept": "application/json",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://play.offshore.virtualregatta.com",
    "priority": "u=1, i",
    "referer": "https://play.offshore.virtualregatta.com/",
    "sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "x-platform": "WebGLPlayer",
    "x-version": "7.0.9"
}

url_sail = url_heading
headers_sail = headers_heading

url_getboatinfos = "https://vro-api-client.prod.virtualregatta.com/getboatinfos"
headers_getboatinfos = {
    "accept": "application/json",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://play.offshore.virtualregatta.com",
    "priority": "u=1, i",
    "referer": "https://play.offshore.virtualregatta.com/",
    "sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "x-api-key": "WL5V/Ck9oPF4RClVbCzk0pBXGnrTrrtMFTCnxn4de3c=",
    "x-platform": "WebGLPlayer",
    "x-playerid": "59dbaacfe7821e29549201de",
    "x-version": "7.0.9"
}

url_getweather = url_heading
headers_getweather = headers_heading

def actions(REQUETE):
    authToken, playerId = auth(MAIL, MDP)
    if REQUETE == "getboatinfos":
        payload = {
            "user_id":"59dbaacfe7821e29549201de",
            "race_id":654,
            "leg_num":1,
            "infos":"engine,bs,ba",
            "country":"FR"
        }
        try:
            resp = requests.post(url_getboatinfos, headers=headers_getboatinfos, json=payload)
            print("HTTP status code:", resp.status_code)
            print("Response body:", resp.text)
        except Exception as e:
            print("Erreur :", e)
    elif REQUETE == "heading":
        payload = {
            "@class": "LogEventRequest",
            "eventKey": "Game_AddBoatAction",
            "race_id": 654,
            "leg_num": 1,
            "actions": [
                {
                    "value": 333,
                    "autoTwa": False,
                    "type": "heading"
                }
            ],
            "ts": get_ts_next_minute(),
            # L'ID de requête peut être quasi quelconque, ou récupéré du jeu.
            "requestId": "638725845444410000_25",
            "authToken": authToken,
            "playerId": playerId
        }
        try:
            resp = requests.post(url_heading, headers=headers_heading, json=payload)
            print("HTTP status code:", resp.status_code)
            print("Response body:", resp.text)
            print(resp.json()["error"]["authToken"])
        except Exception as e:
            print("Erreur :", e)
    elif REQUETE == "sail":
        payload = {
            "@class":"LogEventRequest",
            "eventKey":"Game_AddBoatAction",
            "race_id":706,
            "leg_num":1,
            "actions":[{"value":3,"type":"sail"}],
            "ts": get_ts_next_minute(),
            "requestId":"638727307971430000_42",
            "authToken":authToken,
            "playerId":playerId
        }
        try:
            resp = requests.post(url_sail, headers=headers_sail, json=payload)
            print("HTTP status code:", resp.status_code)
            print("Response body:", resp.text)
        except Exception as e:
            print("Erreur :", e)
    elif REQUETE == "getweather":
        payload = {
            "@class":"LogEventRequest",
            "eventKey":"Game_GetWeather",
            "lat":"-22.26723",
            "lon":"-32.84245",
            "requestId":"638726347053930000_72",
            "authToken":authToken,
            "playerId":playerId
        }
        try:
            resp = requests.post(url_getweather, headers=headers_getweather, json=payload)
            print("HTTP status code:", resp.status_code)
            print("Response body:", resp.text)
        except Exception as e:
            print("Erreur :", e)

actions(REQUETE)