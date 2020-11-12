from pyharmony import client as Client
import sys
import time
import requests
import logging

HARMONY_IP = "192.168.1.30"
PORT = 5222
SLEEP_TIME = 5
REQUEST_URL = "http://127.0.0.1/control"

SWITCH_PROJECTOR = 44913858
SHIELD_PROJECTOR = 44913860
PS3_PROJECTOR = 44913860

# PROJECTOR = "70174191"
ACTIVITIES = [
    SWITCH_PROJECTOR,
    SHIELD_PROJECTOR,
    PS3_PROJECTOR
]

logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO)

def main():
    """Main Function"""
    client = Client.create_and_connect_client(ip_address=HARMONY_IP, port=PORT)
    try:
        previous_activity = 0
        while True:
            activity = client.get_current_activity()
            if activity != previous_activity:
                logging.info(f"Activity Changed: {activity}")
                if activity in ACTIVITIES:
                    logging.info("Extending Projector Screen")
                    requests.post(REQUEST_URL, json={"action": "extend"})
                elif previous_activity in ACTIVITIES:
                    logging.info("Retracting Projector Screen")
                    requests.post(REQUEST_URL, json={"action": "retract"})
                previous_activity = activity
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        client.disconnect()
        sys.exit(0)


if __name__ == "__main__":
    main()