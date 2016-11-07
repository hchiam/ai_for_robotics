####### NOTES: #######

# The function localize takes the following arguments:
#
# world:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# sees:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# moves:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# see_correct:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# move_correct:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up


####### FUNCTIONS: #######

# creates a probability distribution with all locations in 2D world having equal probability:
def uniformDistribution2D(world):
    num_rows = float(len(world))
    num_cols = float(len(world[0]))
    pinit = 1.0 / num_rows / num_cols
    p = [[pinit for row in range(len(world[0]))] for col in range(len(world))]
    return p

# makes probabilities for all locations in world add up to 1:
def normalize(p):
    s = 0
    for i in range(len(p)):
        s += sum(p[i])
    for i in range(len(p)):
        for j in range(len(p[0])):
            p[i][j] = p[i][j] / s
    return p

# "see"s and updates belief probabilities based on what robot thinks it saw:
def see(p, measurement, see_correct):
    q = []
    for i in range(len(p)):
        q.append([])
        for j in range(len(p[0])):
            hit = (measurement == world[i][j])
            # fill q (the updated belief probabilities) with:  p(sensed correct) * previous beliefs * p hit (or miss)
            q[i].append( p[i][j] * (hit * see_correct + (1-hit) * (1-see_correct)) )
    q = normalize(q)
    return q

# "move"s and updates belief probabilities based on how robot thinks it moved:
def move(p, motion, move_correct):
    q = []
    for i in range(len(p)):
        q.append([])
        for j in range(len(p[0])):
            # fill q (the updated belief probabilities) with:  p(motion correct) * previous beliefs + p not move & just stayed
            s = move_correct * p[(i-motion[0]) % len(p)][(j-motion[1]) % len(p[0])]
            s += (1-move_correct) * p[i][j]
            q[i].append(s)
    return q

# figures out where robot is in world based on what it sees as it moves:
def localize(world, measurements, motions, see_correct, move_correct):
    p = uniformDistribution2D(world)
    for i in range(len(motions)):
        p = move(p, motions[i], move_correct);
        p = see(p, measurements[i], see_correct);
    return p

# shows likelihood of robot being in each location in world:
def show(p):
    rows = [ '[' + ','.join(map(lambda x: '{0:.5f}'.format(x),row)) + ']' for row in p ]
    print '[' + ',\n '.join(rows) + ']'


####### INPUTS: #######

world = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
see_correct = 0.7
move_correct = 0.8

####### LOCALIZE based on inputs: #######

p = localize(world, measurements, motions, see_correct, move_correct)


####### ANSWER: #######

show(p)


#############################################################
# For the following test case, your output should be
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

# (it most likely moved down along the green path and stopped at the end)