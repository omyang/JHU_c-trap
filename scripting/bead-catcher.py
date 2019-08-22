from bluelake import traps, timeline, fluidics, stage, pause, reset_force

pt=0.3

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

def catch_beads(min_score = 30) :
    target_traps = traps[:2]

    # option 2
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
    return 1


#test
setpressure(0.3)
fluidics.open(1,2,3,6)
catch_beads(80)
