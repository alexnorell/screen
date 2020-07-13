#!/usr/bin/env python3
"""Motorized Project Screen Class and Control Application"""
import argparse
import asyncio
import sys

try:
    # pylint: disable=import-error
    import gpiozero
    MOCK = False
except ModuleNotFoundError:
    MOCK = True

RELAY_1_PIN = 26  # Up
RELAY_2_PIN = 20  # Down
RELAY_3_PIN = 21  # Neutral


class MotorizedScreen():
    """Motorized project screen"""
    def __init__(self, neutral=RELAY_3_PIN, up=RELAY_1_PIN, down=RELAY_2_PIN):
        if not MOCK:
            self._neutral = gpiozero.DigitalOutputDevice(neutral)
            self._up = gpiozero.DigitalOutputDevice(up)
            self._down = gpiozero.DigitalOutputDevice(down)
        else:
            self._neutral = GPIOMock(neutral)
            self._up = GPIOMock(up)
            self._down = GPIOMock(down)
        self.running_task = None  # Stores current async task being run

    async def retract(self, duration=30):
        """Raise the projector screen"""
        self._neutral.on()
        self._up.on()
        await asyncio.sleep(duration)
        self._up.off()
        self._neutral.off()

    async def extend(self, duration=30):
        """Extend the projector screen"""
        self._neutral.on()
        self._down.on()
        await asyncio.sleep(duration)
        self._down.off()
        self._neutral.off()

    async def stop(self):
        """Stop the screen movement"""
        if self.running_task and not self.running_task.done():
            self.running_task.cancel()
            self.running_task = None
        self._down.off()
        self._up.off()
        self._neutral.off()


class GPIOMock():
    """Mock of gpio functions used in MotorizedScreen"""
    #pylint: disable=invalid-name
    def __init__(self, pin):
        """Initialize with pin information"""
        self.pin = pin

    def on(self):
        """Turn on"""
        print(f"Turn {self.pin} on")

    def off(self):
        """Turn off"""
        print(f"Turn {self.pin} off")


def parse_arguments():
    """Parse command line arguments to control screen"""
    parser = argparse.ArgumentParser(description="Projector Screen Control")
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--retract",
                         "--up",
                         "--raise",
                         action="store_true",
                         help="Raise the projector screen")
    actions.add_argument("--extend",
                         "--down",
                         "--lower",
                         action="store_true",
                         help="Lower the projector screen")
    args = parser.parse_args()
    return args


def main():
    """If running as standalone application, this is what is ran"""
    args = parse_arguments()
    screen = MotorizedScreen()
    if args.extend:
        task = screen.extend
        action = "extend"
    elif args.retract:
        task = screen.retract
        action = "retract"
    try:
        asyncio.run(task())
        print(f"Screen {action}ed.")
    except KeyboardInterrupt:
        asyncio.run(screen.stop())
        print(f"Screen {action} cancelled")
        sys.exit(1)


if __name__ == "__main__":
    main()
