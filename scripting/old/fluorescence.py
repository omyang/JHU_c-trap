from bluelake import Trap, stage, fluidics, pause, power, timeline,reset_force, confocal

reset_force()
timeline.mark_begin("FD1")

while Distancebeads.latest_value <25:
    trap1.move_by(dx=3, speed=8)
    confocal.start_scan()  # start the active configuration

    # wait for scan to finish
    pause(1)
    while confocal.is_scanning:
        pause(1)

timeline.mark_end()

print("Done!")