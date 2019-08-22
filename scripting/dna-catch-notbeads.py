#trapping dna with ping pong automation
#make sure you catch beads first

from bluelake import Trap, stage, fluidics, pause, reset_force, timeline

trap = Trap("1", "XY")
pt=0.3

#functions that we need to catch DNA
def pingpongforce():
    trap.move_by(dx=10,speed=5.5)
    ppf=trap.current_force
    trap.move_by(dx=-10,speed=6.5)
    return ppf

def gohome():
    trap.move_to(waypoint="catch DNA",speed=7)
    print("trap1 bead is home")

def pressurecycle():
    while fluidics.pressure < .6:
        fluidics.increase_pressure()
        pause(pt) #important!
    while fluidics.pressure > 0.24:
        fluidics.decrease_pressure()
        pause(pt) #important!
    print("pressure cycled")

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

def movetoch4():
    fluidics.stop_flow()
    stage.move_to("J1")
    stage.move_to("Ch1")
    setpressure(0.1)
    fluidics.open(1,2,3,4,6)
    reset_force()
    print("setup should be ready to go")

#THIS IS THE START OF THE MAIN -------------------------------

#turn on fluidics
fluidics.open(1, 2, 3, 6)
# set up the pressure
setpressure(0.22)

#set traps at initial position and reset force
gohome()
reset_force()
print("initialized position")

#initialize variables
pforce_old=pingpongforce()
pforce=pforce_old
caught=0
attempts=1
print("initialized variables ("+str(round(pforce_old,2)))

#moving into dna channel and starting pingpong
while caught!=1:
    print(" we've attempted "+str(attempts)+" times")
    print("    old force ="+str(round(pforce_old,2)))
    stage.move_to("DNA")
    pause(0.5)
    stage.move_to("buffer")
    pforce=pingpongforce()
    #print("    new force ="+str(round(pforce)))
    if (pforce_old*0.8)>pforce or pforce>(pforce_old*1.2):
          caught=1
    else:
          pforce_old=pforce
          attempts+=1
    if (attempts%15)==0:
        pressurecycle()

print("hopefully we finished")

#hopefully caught something, move to buffer channel and reset all
stage.move_to("buffer")
gohome()
fluidics.stop_flow()
reset_force()
print("hopefully in the buffer channel with all reset")

#if want to move to ch4 to ready for experiment start
movetoch4()
trap.move_to(waypoint="stretched",speed=3)
