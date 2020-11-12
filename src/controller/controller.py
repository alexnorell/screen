"""Web controller for motorized screen"""
import asyncio
import logging

from quart import Quart, request, jsonify, render_template
from quart_minify.minify import Minify

from screen import MotorizedScreen

app = Quart(__name__)
Minify(app=app)
logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO)

SCREEN = MotorizedScreen()


@app.route("/")
async def _landing():  # pylint: disable=unused-variable
    """Landing Page"""
    moving = SCREEN.running_task is not None
    template = await render_template("index.html", status={"moving": moving})
    return template


@app.route("/control", methods=["POST"])
async def _control():  # pylint: disable=unused-variable
    """Control API endpoint"""
    request_json = await request.get_json()
    action = request_json["action"]
    if not action or action not in ["extend", "retract", "stop"]:
        return jsonify(success=False)
    # Screen in motion, and a new request is made, return an error
    if SCREEN.running_task and action in ["extend", "retract"]:
        error_message = "Screen in motion. Must stop or complete"
        logging.error(error_message)
        return jsonify(error=error_message, success=False)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
