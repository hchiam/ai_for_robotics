# MEASUREMENT (SENSING) UPDATE STEP OF KALMAN FILTER:
# (BAYES RULE MULTIPLICATION)

# Write a program to update your mean and variance
# when given the mean and variance of your belief
# and the mean and variance of your measurement.
# This program will update the parameters of your
# belief function.

def update(mean1, var1, mean2, var2):
    new_mean = (mean1*var2 + mean2*var1) / (var1+var2) # NOTE: m1*v2 + m2*v1, AND NOT: m1*v1 + m2*v2
    new_var = 1 / (1/var1 + 1/var2)
    return [new_mean, new_var]

print update(10., 8., 13., 2.)


# MOTION UPDATE STEP OF KALMAN FILTER:
# (TOTAL PROBABILITY ADDITION)

# Write a program that will predict your new mean
# and variance given the mean and variance of your 
# prior belief and the mean and variance of your 
# motion. 

# PREDICTION STEP:

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

print predict(10., 4., 12., 4.)