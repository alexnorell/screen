"""Control screen based on Harmony Activity"""
import logging
import sys
import time

import requests
from pyharmony import client as Client

HARMONY_IP = "192.168.1.30"
PORT = 5222
SLEEP_TIME = 5
REQUEST_URL = "http://127.0.0.1/control"
RESET_TIME = 60 * 60

SWITCH_PROJECTOR = 44913858
SHIELD_PROJECTOR = 44913860
PS3_PROJECTOR = 44913860

# PROJECTOR = "70174191"
ACTIVITIES = [SWITCH_PROJECTOR, SHIELD_PROJECTOR, PS3_PROJECTOR]

logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO)


def main():
    """Main Function"""
    client = None
    start_time = time.time()
    try:
        previous_activity = 0
        while True:
            if not client or time.time() > (start_time + RESET_TIME):
                start_time = time.time()
                if client:
                    logging.info("Reset client connection")
                logging.info("Connect harmony client to %s:%s", HARMONY_IP, PORT)
                client = Client.create_and_connect_client(
                    ip_address=HARMONY_IP, port=PORT)
            activity = client.get_current_activity()
            if activity != previous_activity:
                logging.info("Activity Changed: %s", activity)
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
