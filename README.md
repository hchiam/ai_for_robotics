# ai_for_robotics
code based on Udacity course AI for Robotics

## Notes:

### Localization:
localization : initial belief --> sense --> move --> sense --> move

i.e. : initial belief --> ( back & forth : sense <--> move )

move loses info

sense gains info

* belief = probability
* sense = multiplication followed by normalization
* move = addition (convolution)

### Bayes Rule for Localization:
p(Xi|M) = p(Xi) * p(M|Xi) / p(M)
* (let Xi = probability of being at a given position xi)
* (let M = probability of getting a given measurement)

p(Xi|M) = prior * measurement probability / p(M)

p(M) = normalization constant

p(M) = sum over i of ( p(Xi) * p(M|Xi) )