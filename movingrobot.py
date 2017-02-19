# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
#
# Your program should print out the result of
# your two sense measurements.
#
# Don't modify the code below. Please enter
# your code at the bottom.

from math import *
import random



landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))



####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

print("\nBasic robot:\n")

myrobot = robot()
# 30, 50, pi/2
myrobot.set(30.0, 50.0, pi/2)
# -pi/2, 15
myrobot = myrobot.move(-pi/2, 15.0)
# sense
print(myrobot.sense())
# -pi/2 10
myrobot = myrobot.move(-pi/2, 10.0)
# sense
print(myrobot.sense())

# output should be around: 
# [39, 46, 39, 46]
# [32 ,53 ,47 ,40]

print("\nRobot with noise:\n")

myrobot = robot()
myrobot.set_noise(5.0, 0.1, 5.0) # add noise for forward, turn, sense
myrobot.set(30.0, 50.0, pi/2)
myrobot = myrobot.move(-pi/2, 15.0)
print(myrobot.sense())
myrobot = myrobot.move(-pi/2, 10.0)
print(myrobot.sense())

print("\nCreate n particles with noise (so a later calculation doesn't divide by 0):\n")

n = 1000
p = [] # list of particles

for i in range(n):
    r = robot()
    r.set_noise(0.05, 0.05, 5.0)
    p.append(r)
    # this has the same effect as:
    # x = random.random() * world_size
    # y = random.random() * world_size
    # a = random.random() * 2.0 * pi
    # p.append([x,y,a])

print(len(p))

print("\nMove all particles:\n")

# turn 0.1, move 5
for particle in p:
    particle = particle.move(0.1, 5.0)

print("(Done.)")

print("\nApply importance weights; get guess particle 'fitness' levels:\n")

# make use of measurement_prob(measurement)
w = []

for particle in p:
    w.append(particle.measurement_prob(particle.sense()))

print(str(len(w)) + " importance weights created")

print("\nResample particles based on importance weights weighing probability of sampling:\n")

print("(Using re-sampling wheel for linear time.)")

# alternate description:
# https://www.youtube.com/watch?v=tvNPidFMY20

p2 = []
randomStartIndex = int(random.random() * n) # get a random index out of n possible indices
cumuDistribAroundClock = 0.0 # initialize running variable of how far around the "pie" we've traveled
maxWt = max(w)

# rename variables for shorter names in the following loop
index = randomStartIndex
beta = cumuDistribAroundClock

# get n particles from the old list of particles (with bigger "pie slices" being more likely to get more repeats)
for i in range(n):
    # go around the "pie"
    beta += random.random() * 2.0 * maxWt # random.random() is between 0 and 1, so makes beta between 0 and 2 x max(wt)
    # get next particle INDEX with particle WEIGHT that happens to "CAPTURE" BETA (the "pie spinner")
    while beta > w[index]:
        beta -= w[index]
        index = (index + 1) % n # check the next "slice" of the "pie"
    # add that particle to the new, re-sampled particles list
    p2.append(p[index])

p = p2 # update to re-sampled particles list

print("(Done.)")
