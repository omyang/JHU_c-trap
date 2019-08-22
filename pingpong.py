#import bluelake_remote
from bluelake import Trap, pause, log

trap1 = Trap("1", "XY")

def pingpong(distance_delta_um, period_ms, speed):
    while True:
        trap1.move_by(dx=+distance_delta_um, speed=speed)
        pause(period_ms / 1000 / 2)
        log("ping")
        trap1.move_by(dx=-distance_delta_um, speed=speed)
        pause(period_ms / 1000 / 2)
        log("pong")

log("Running pingpong script")
pingpong(distance_delta_um=0.008, period_ms=50, speed=0)
