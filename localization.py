# code based on Udacity course AI for Robotics

# code capturing the core of how Google's self-driving car localization works!


### notes:

# localization : initial belief --> sense --> move --> sense --> move
    # i.e. : initial belief --> ( back & forth : sense <--> move )
# move loses info
# sense gains info

# belief = probability
# sense = multiplication followed by normalization
# move = addition (convolution)


### variables, setup:

p = [0.2, 0.2, 0.2, 0.2, 0.2] # start with uniform probability distribution over 5 positions

world = ['line', 'road', 'road', 'road', 'line']
measurements = ['road','road'] # what it sees at different time stamps
motions = [1,1] # how far it tries to move at different time stamps

# probability adjustments for what is measured or "seen":
pHit = 0.6
pMiss = 0.2

# probability adjustments for motion:
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1


### functions, setup still:

def sense(p, m): # p=probabilities ; m=measurement
    # adjust probabilities (prior --> posterior belief probability values):
    q = []
    for i in range(len(p)):
        hit = (m == world[i])
        q.append( p[i] * pHit if hit else p[i] * pMiss if not hit else 0 )
    # normalize (make probabilities add up to 1):
    qSum = sum(q)
    for i in range(len(q)):
        q[i] /= qSum
    return q

def move(p, u): # p=probabilities ; u=units moved
    q = []
    for i in range(len(p)):
        pSum = pExact * p[(i-u)%len(p)]
        pSum += pUndershoot * p[(i-u+1)%len(p)]
        pSum += pOvershoot * p[(i-u-1)%len(p)]
        q.append(pSum)
    return q


### using the variables and functions:

print 'prior ='
print p # prior belief probability distribution for localization

for i in range(len(measurements)):
    p = sense(p, measurements[i])
    p = move(p, motions[i])

print 'posterior ='
print p # posterior belief probability distribution for localization