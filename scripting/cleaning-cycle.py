#cleaning pressure cycler
#because I don't want to set a timer
#a 3min high pressure + 27min low pressure, then vent and close

from bluelake import fluidics, pause

def setpressure(pres):
    curpres=fluidics.pressure
    if curpres<pres:
        while fluidics.pressure < pres:
            fluidics.increase_pressure()
            pause(0.1) #important!
    else:
        while fluidics.pressure > pres:
            fluidics.decrease_pressure()
            pause(0.1) #important!

def timeprogression(time,numsteps):
    stepsize=round(time/numsteps,2)
    for i in range(1,numsteps+1):
        pause(stepsize)
        print(" "+str(round(i*stepsize*100/time)) + "% of time has elapsed")


#MAIN ------------------------------------------
print("starting high pressure")
setpressure(1.1)
fluidics.open(1,2,3,4,5,6)
timeprogression(60*3,3)

print("high done, starting low pressure")
setpressure(0.4)
timeprogression(60*10,14)

fluidics.stop_flow()
print("   should be done and vented")
