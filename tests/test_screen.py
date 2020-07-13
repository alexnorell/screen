"""Test the screen python module"""
# pylint: disable=unused-variable
import screen


def test_extend():
    """Test the extend method to see if if crashes or changes"""
    test_screen = screen.MotorizedScreen()
    screen.screen.asyncio.run(test_screen.extend(0))


def test_retract():
    """Test the retract method to see if if crashes or changes"""
    test_screen = screen.MotorizedScreen()
    screen.screen.asyncio.run(test_screen.extend(0))
