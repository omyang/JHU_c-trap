#cleaning pressure cycler
#because I don't want to set a timer
#a 3min high pressure + 27min low pressure, then vent and close

from bluelake import fluidics, pause

def setpressure(pres):
    curpres=fluidics.pressure
    if curpres<pres:
        while fluidics.pressure < pres:
            fluidics.increase_pressure()
            pause(0.7) #important!
    else:
        while fluidics.pressure > pres:
            fluidics.decrease_pressure()
            pause(0.7) #important!


#MAIN ------------------------------------------
print("starting high pressure")
setpressure(1.1)
fluidics.open(1,2,3,4,5,6)
pause(60*3)

print("high done, starting low pressure")
setpressure(0.4)
pause(60*27)
fluidics.stop_flow()

print("   should be done and vented")
