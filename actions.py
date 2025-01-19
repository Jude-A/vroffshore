from AutoBoat import RACE_ID, LEG_NUM
from ts import get_ts_next_minute
import headers as hd

import requests
import csv

def parsee():
    input_file = "VRZEN.csv"
    output_file = "caps.csv"

    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['Date', 'Heure', 'HDG', 'Voile']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',')

        writer.writeheader()
        for row in reader:
            dateheure = row['DateHeure'].split(" ")
            filtered_row = {
                'Date': dateheure[0],
                'Heure': dateheure[1],
                'HDG': row['HDG'],
                'Voile': row['Voile']
            }
            writer.writerow(filtered_row)

    print(f"Filtered data has been written to {output_file}")

def parse(row):
    date_str, hour_minute_str, heading_str, sail_str = row[0], row[1], row[2], row[3]
    annee_str, mois_str, jour_str = date_str.split("-")
    hour_str, minute_str = hour_minute_str.split(":")
    minute, hour, jour, mois, annee, heading = int(minute_str), int(hour_str), int(jour_str), int(mois_str), int(annee_str), int(heading_str)

    return minute, hour, jour, mois, annee, heading, sail_str

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
        print("Authentifier")
        return auth_token, userId
    except Exception as e:
        print("Erreur :", e)

def send_heading_now(heading, hour, minute, authToken, playerId):
    payload = {
        "@class": "LogEventRequest",
        "eventKey": "Game_AddBoatAction",
        "race_id": RACE_ID,
        "leg_num": LEG_NUM,
        "actions": [
            {
                "value": heading,
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
        resp = requests.post(hd.url_heading, headers=hd.headers_heading, json=payload)
        print(f"| [Waypoint] {hour:02}:{minute:02} | Le cap est fixé sur {heading}")
        print("| -> Requête status code:", resp.status_code)
        if resp.status_code == 403:
            return resp.status_code, resp.json()["error"]["authToken"]
        else:
            return resp.status_code, None
    except Exception as e:
        print("Erreur :", e)

def get_sail_value(sail):
    sail_mapping = {
        "Code 0": 5,
        "Jib": 1,
        "Spi": 2,
        "Spi leger": 7,
        "Spi lourd": 6,
        "Genois leger": 4,
        "Trinquette": 3
    }
    return sail_mapping.get(sail, None)

def send_sail_now(sail, hour, minute, authToken, playerId):
    s = get_sail_value(sail) 
    payload = {
        "@class": "LogEventRequest",
        "eventKey": "Game_AddBoatAction",
        "race_id": RACE_ID,
        "leg_num": LEG_NUM,
        "actions": [
            {
                "value": s,
                "type": "sail"
            }
        ],
        "ts": get_ts_next_minute(),
        # L'ID de requête peut être quasi quelconque, ou récupéré du jeu.
        "requestId": "638725845444410000_25",
        "authToken": authToken,
        "playerId": playerId
    }
    try:
        resp = requests.post(hd.url_sail, headers=hd.headers_sail, json=payload)
        # print("Response body:", resp.text)
        print(f"| [SAIL] {hour:02}:{minute:02} | La voile {sail} est mise")
        print(f"| -> Requête status code:", resp.status_code)
    except Exception as e:
        print("Erreur :", e)

# def get_boat_info():
#     payload = {
#         "user_id": PLAYER_ID,
#         "race_id": RACE_ID,
#         "leg_num": LEG_NUM,
#         "infos":"bs,track,engine",
#         "country":"FR"
#     }
#     try:
#         resp = requests.post(hd.url_heading, headers=hd.headers_getboat, json=payload)
#         print("HTTP status code:", resp.status_code)
#         print("Response body:", resp.text)
#     except Exception as e:
#         print("Erreur :", e)
