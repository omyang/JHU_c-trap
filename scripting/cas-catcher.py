#to move from imaging channel to buffer channel slowly
#assumptions:start from 'buffer' channel at least?

from bluelake import Trap, stage, fluidics, pause, reset_force

trap = Trap("1", "XY")
pt=0.1
spd=35

#functions that may be helpful
def setpressure(pres):
    curpres=fluidics.pressure
    if curpres<pres:
        while fluidics.pressure < pres:
            fluidics.increase_pressure()
            pause(pt) #important!
    else:
        while fluidics.pressure > pres:
            fluidics.decrease_pressure()
            pause(pt) #important!

# MAIN-----------------------------------------------------------
print("moving to ch1")
stage.move_to("J1",speed=spd)
stage.move_to("Ch1",speed=spd)

print("waiting...")
pause(10)
print("done waiting, time to move")

stage.move_to("J1",speed=spd)
stage.move_to("buffer",speed=spd)
print("done moving, start imaging!")
