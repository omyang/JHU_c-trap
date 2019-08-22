# Zsombor 
# bead cathcing, dna binding, check force, then check for single tether with force only
# parts of the code are copy pasted from somewhere else, single tether catching might be the first
# or at least I couldn't find anything


from bluelake import traps, timeline, fluidics, stage, pause, reset_force
from numpy import std
import time

def goto_distance(target_distance,move_speed = 8, force_limit=10000):
    trap1, trap2 = traps[:2]
    distance = timeline["Distance"]["Distance 1"]
    dx = distance.latest_value - target_distance

    while abs(dx) > 0.2:
        if trap2.current_force > force_limit:
            break

        if dx <= 0:
            trap1.move_by(dx=+abs(dx)*0.8, speed=move_speed) # MAYBE play around with this
        else:
            trap1.move_by(dx=-abs(dx)*0.8, speed=move_speed)
        dx = distance.latest_value - target_distance
        # print(dx)
    # print("till here")
    pause(1)

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


# # NEED a function like this
def check_for_beads(min_score = 80):
    # check if you still have beads inside
    bead1 = timeline['Tracking Match Score']['Bead 1']
    bead2 = timeline['Tracking Match Score']['Bead 2']
    bead_scores = [bead1, bead2]
    if any(bead.latest_value < min_score for bead in bead_scores):
        return 0
    elif any(bead.latest_value == 0 for bead in bead_scores):
        return 0
    else:
        return 1


def is_single_tether(max_force=70, min_force=30, backward_speed = 1):
    # min_forcce depemds on the rate of flow, especially when you have flow
    # make sure that you don't have bubbles inside the system
    trap1, trap2 = traps[:2]
    distance = timeline["Distance"]["Distance 1"]
    goto_distance(10)
    print("traps are 10 um apart")
    trap1.move_by(dx = -3, speed = backward_speed) # MAYBE play with this
    reset_force()
    pause(0.5) # MAYBE play with this
    baseline_force = trap1.current_force
    # print('baseline force')
    # print(baseline_force)
    trap1.move_by(dx = 3, speed = 5) # MAYBE play with this
    force_list = []
    ii = 0
    # while distance.latest_value < 26: # MAYBE play with this, not sure how long you can stretch DNA
    while ii<38: # MAYBE play with this, not sure how long you can stretch DNA
        ii += 1
        trap1.move_by(dx = 0.5, speed = 5)
        # print('trap1 force')
        # print(trap1.current_force)
        current_force = abs(baseline_force - trap1.current_force)
        # print(current_force)
        force_list.append(current_force)
        if current_force > max_force:
            print("Multiple tethers found")
            return 2
        # elif distance.latest_value > 16:
        elif ii > 18:
            if current_force > min_force:
                # print('stdev of past 10 forces')
                # print(std(force_list[-10:]))
                if std(force_list[-10:]) < 2:
                    print("Single tether potentially found")
                    trap1.move_by(dx = -16, speed = 5)
                    return 1
    print("No tethers found")
    trap1.move_by(dx = -16, speed = 5)
    return 0



# get beads from the channel
def bead_DNA_complex_setup():
    fluidics.open(1, 2, 3, 6)
    fluidics.close(4, 5)
    pause(5) # wait for flow to start
    stage.move_to("beads")
    print("Moved to Beads channel")
    catch_beads(80)
    print("Beads are trapped")
    # stage.move_to("DNA")
    # print("Moved to DNA channel")
    # pause(5) ## DEFINITELY have to play with this based on DNA concentration/flow rate
    # print('till here')
    stage.move_to("buffer")
    print("Moved to Buffer channel")


print('start executing script')

# set up the pressure
while fluidics.pressure < .20:
    fluidics.increase_pressure()
    pause(1) #important!
pause(5)


single_tether_count = 0
mult_tether_count = 0
number_of_tries = 0

# this is going to be a for loop that can be broken
for jj in range(10):

# while single_tether_count < 100:

    start = time.time()
    number_of_tries += 1
    bead_DNA_complex_setup()
    end = time.time()

    print("Assay assembly: ", end-start, " seconds")

    are_beads = check_for_beads()
    print(are_beads)
    if are_beads == 0:
        continue
    # goto_distance(10) # might be redundant
    # check for single-tethers WITH FLOW
    for i in range(3):
        tether_flow = is_single_tether()
        mult_tether = 0
        if tether_flow == 1:
            break
        if tether_flow == 2:
            mult_tether = 1
            break

    if mult_tether == 1:
        mult_tether_count += 1
        continue

    if tether_flow == 0:
        print("No tethers found, going for new beads")
        continue

    # see if it's a single tether WITHOUT FLOW
    fluidics.close(1, 2, 3, 4, 5, 6)
    pause(3) # wait for flow to stop

    for i in range(3):
        tether_flow = is_single_tether(backward_speed=5)
        mult_tether = 0
        if tether_flow == 1:
            break
        if tether_flow == 2:
            mult_tether = 1
            break

    if mult_tether == 1:
        mult_tether_count += 1
        continue

    if tether_flow == 0:
        print("No tethers found, going for new beads")
        continue

    single_tether_count += 1
    
    print('Number of single tethers (still running):', single_tether_count)
    print("Number of multiple tethers (still running):", mult_tether_count)
    print("Number of tries (still running):", number_of_tries)


    ##### ----- the loop only gets here if there're two beads caught plus a single tether in-between them
    goto_distance(7)
    timeline.mark_begin("Single tether")
    print("Single tether most likely found")
    trap1, trap2 = traps[:2]
    trap1.move_by(dx=15, speed=2)
    pause(2)
    trap1.move_by(dx=-15, speed=2)
    # is_single_tether()
    timeline.mark_end()
    goto_distance(10)
    

print("Time elapsed: ", end-start, " seconds")
print('Number of single tethers:', single_tether_count)
print("Number of multiple tethers:", mult_tether_count)
print("Number of tries:", number_of_tries)


