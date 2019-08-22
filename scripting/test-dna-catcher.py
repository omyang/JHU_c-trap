#trapping dna with ping pong automation
#make sure you catch beads first

from bluelake import Trap, Stage, Fluidics, pause, reset_force

trap = Trap("1", "XY")

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
        pause(0.7) #important!
    while fluidics.pressure > 0.24:
        fluidics.decrease_pressure()
        pause(0.7) #important!
    print("pressure cycled")

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

def movetoch4():
    fluidics.stop_flow()
    stage.move_to("J1")
    stage.move_to("Ch1")
    setpressure(0.1)
    fluidics.open(1,2,3,4,6)
    print("setup should be ready to go")

#THIS IS THE START OF THE MAIN -------------------------------
#turn on fluidics
fluidics.open(1, 2, 3, 6)
# set up the pressure
while fluidics.pressure < .25:
    fluidics.increase_pressure()
    pause(1) #important!

#set traps at initial position and reset force
gohome()
reset_force()
print("initialized position")

#initialize variables
pforce_old=pingpongforce()
pforce=pforce_old
caught=0
attempts=1
print("initialized variables")

#moving into dna channel and starting pingpong
stage.move_to("DNA")
print("stage moved")

while caught!=1:
    print(" we've attempted "+str(attempts)+" times")
    print("    old force ="+str(round(pforce_old)))
    pause(0.8)
    pforce=pingpongforce()
    #print("    new force ="+str(round(pforce)))
    if (pforce_old*0.85)>pforce or pforce>(pforce_old*1.15):
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
