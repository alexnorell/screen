import pytest
import screen 

def test_extend():
    test_screen = screen.screen.MotorizedScreen()
    test_screen.extend()


def test_retract():
    test_screen = screen.screen.MotorizedScreen()
    test_screen.retract()
