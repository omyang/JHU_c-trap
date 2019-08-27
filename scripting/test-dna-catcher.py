#trapping dna with ping pong automation
#will catch your beads

from bluelake import Trap, stage, fluidics, pause, reset_force, timeline, traps

trap = Trap("1", "XY")
pt=0.1
echannel=1 #change this to 1 if you want to end in an experiment channel
dnadwell=3 #how long to dwell in dna channel (sec)

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
    while fluidics.pressure > 0.22:
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

def beadtest():
    bead1 = timeline['Tracking Match Score']['Bead 1']
    bead2 = timeline['Tracking Match Score']['Bead 2']
    bead_scores = [bead1, bead2]
    if all(bead.latest_value > 0.85 for bead in bead_scores):
        print("you already have beads")
        return 1
    else:
        print("gotta get beads")
        return 0

def catch_beads(min_score = 30) : #from Zsombor
    stage.move_to("beads")
    target_traps = traps[:2]

    target_traps[1].clear()
    target_traps[0].clear()
    bead1 = timeline['Tracking Match Score']['Bead 1']
    bead2 = timeline['Tracking Match Score']['Bead 2']
    bead_scores = [bead1, bead2]

    while any(bead.latest_value < min_score for bead in bead_scores):
        if any(0 < bead.latest_value < min_score for bead in bead_scores):
            for trap in target_traps:
                trap.clear()  # bad beads
                print('bad beads')
            pause(1)
    print("beads should be caught")

#THIS IS THE START OF THE MAIN -----------------------------------------

#check for beads first
bt=beadtest()
if bt==0:
    setpressure(0.3)
    fluidics.open(1,2,3,6)
    stage.move_to("beads")
    catch_beads(82)
else:
    #turn on fluidics
    fluidics.open(1, 2, 3, 6)

# set up the pressure
stage.move_to("buffer")
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
print("initialized variables (old="+str(round(pforce_old,2))+")")

#moving into dna channel and starting pingpong
while caught!=1:
    print(" we've attempted "+str(attempts)+" times")
    #print("    new force ="+str(round(pforce,2)))
    stage.move_to("DNA")
    pause(dnadwell)
    stage.move_to("buffer")
    pforce=pingpongforce()
    print("    new force ="+str(round(pforce,2)))
    if (pforce_old*0.77)>pforce or pforce>(pforce_old*1.23):
          caught=1
    else:
          pforce_old=pforce
          if (attempts%15)==0:
              pressurecycle()
          attempts+=1

print("hopefully we finished")

#hopefully caught something, move to buffer channel and reset all
stage.move_to("buffer")
gohome()
fluidics.stop_flow()
reset_force()
print("in the buffer channel with all reset")

#if want to move to ch4 to ready for experiment start
if echannel==1:
    movetoch4()
    trap.move_to(waypoint="stretched",speed=3)
    print('ready to image!')
