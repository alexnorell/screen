"""Control screen based on Harmony Activity"""
import logging
import sys
import time

import requests
import redis
from pyharmony import client as Client

HARMONY_IP = "192.168.1.30"
PORT = 5222
SLEEP_TIME = 0.01
REQUEST_URL = "http://127.0.0.1/control"
RESET_TIME = 60 * 60

SWITCH_PROJECTOR = 44913858
SHIELD_PROJECTOR = 44913860
PS3_PROJECTOR = 44913860
OFF = -1

# PROJECTOR = "70174191"
ACTIVITIES = [SWITCH_PROJECTOR, SHIELD_PROJECTOR, PS3_PROJECTOR]

logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.DEBUG)


def handle_change(activity):
    """Handle am activity change and adjust screen"""
    activity_string = f"Activity Changed: {activity}"
    logging.info(activity_string)
    previous_activity = int(_R.get("activity"))
    previous_activity_string = f"Previous Activity: {previous_activity}"
    logging.info(previous_activity_string)
    if activity in ACTIVITIES and previous_activity not in ACTIVITIES:
        control_screen("extend")
    elif activity == OFF:
        control_screen("retract")
    elif previous_activity in ACTIVITIES and activity not in ACTIVITIES:
        control_screen("retract")
    _R.set("activity", activity)


def control_screen(action):
    logging.info("%sing Projector Screen" % action.title())
    requests.post(REQUEST_URL, json={"action": action})
    _R.set("state", f"{action}ed")


def create_client():
    log_message = f"Connect harmony client to {HARMONY_IP}:{PORT}"
    logging.info(log_message)
    client = Client.create_and_connect_client(ip_address=HARMONY_IP,
                                              port=PORT,
                                              activity_callback=handle_change)
    activity = client.get_current_activity()
    _R.set("activity", activity)
    if activity in ACTIVITIES:
        state = "extended"
    else:
        state = "retracted"
    _R.set("state", state)
    return client


def main():
    """Main Function"""
    client = None
    start_time = time.time()
    try:
        while True:
            if not client or time.time() > (start_time + RESET_TIME):
                start_time = time.time()
                if client:
                    logging.info("Reset client connection")
                    client.disconnect()
                client = create_client()
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        client.disconnect()
        sys.exit(0)


if __name__ == "__main__":
    _R = redis.Redis(host='localhost', port=6379, db=0)
    main()
