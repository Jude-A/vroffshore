import time
import datetime
import requests
import csv

from ts import *
import headers as hd
from actions import *

MAIL = ""
MDP = ""

RACE_ID = 654
LEG_NUM = 1

def main():

    csv_file = "caps.csv"

    AUTH_TOKEN, USER_ID = auth(MAIL, MDP)

    parsee()

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        flag = 0
        previous_heading = None
        previous_sail = None
        for row in reader:
            minute, hour, day, month, year, heading, sail = parse(row)

            target_ts = get_ts_for_specific_time(hour, minute, day, month, year) - 60000
            now_ts = int(time.time()*1000)

            if target_ts < now_ts:
                print(f"| [Waypoint] {hour:02}:{minute:02} déjà passé.")
                previous_heading = heading
                previous_sail = sail
                continue

            if flag == 0:
                code, err = send_heading_now(previous_heading, datetime.datetime.now().hour, datetime.datetime.now().minute, AUTH_TOKEN, USER_ID)
                send_sail_now(previous_sail, datetime.datetime.now().hour, datetime.datetime.now().minute, AUTH_TOKEN, USER_ID)
                if code == 403 and err == "INVALID":
                    AUTH_TOKEN, USER_ID = auth(MAIL, MDP)
                    send_heading_now(previous_heading, datetime.datetime.now().hour, datetime.datetime.now().minute, AUTH_TOKEN, USER_ID)
                    send_sail_now(previous_sail, datetime.datetime.now().hour, datetime.datetime.now().minute, AUTH_TOKEN, USER_ID)
                flag = 1
            
            
            while int(time.time() * 1000) < target_ts:
                time.sleep(60)

            if heading != previous_heading:
                code, err = send_heading_now(heading, hour, minute, AUTH_TOKEN, USER_ID)
            if sail != previous_sail:
                send_sail_now(sail, hour, minute, AUTH_TOKEN, USER_ID)
            if code == 403 and err == "INVALID":
                AUTH_TOKEN, USER_ID = auth(MAIL, MDP)
                if heading != previous_heading:
                    send_heading_now(heading, hour, minute, AUTH_TOKEN, USER_ID)
                if sail != previous_sail:
                    send_sail_now(sail, hour, minute, AUTH_TOKEN, USER_ID)

            previous_heading = heading
            previous_sail = sail
      
if __name__ == "__main__":
    main()
