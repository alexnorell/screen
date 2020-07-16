import asyncio
from quart import Quart, request, jsonify
import logging

from screen import MotorizedScreen

app = Quart(__name__)
logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

SCREEN = MotorizedScreen()


@app.route('/')
async def landing():
    moving = SCREEN.running_task is not None
    return {"moving": moving}


@app.route('/control', methods=["POST"])
async def control():
    action = (await request.get_json())["action"]
    if not action or action not in ["extend", "retract", "stop"]:
        return jsonify(success=False)
    # Screen in motion, and a new request is made, return an error
    if SCREEN.running_task and action in ["extend", "retract"]:
        return jsonify(error="Screen in motion. Must stop or complete",
                       success=False)
    if action == "stop" and SCREEN.running_task is not None:
        logging.debug("Stop running action")
        SCREEN.running_task.cancel()
    actions = {
        "extend": SCREEN.extend,
        "retract": SCREEN.retract,
        "stop": SCREEN.stop
    }
    action_task = actions.get(action)
    task = asyncio.ensure_future(action_task())
    SCREEN.running_task = task
    return jsonify(success=True)


app.run()
