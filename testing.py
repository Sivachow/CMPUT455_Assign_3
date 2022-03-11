# Cmput 455 sample code
# Sampling from a discrete probability distribution
# Written by Martin Mueller

import random

# probabilities should add up to 1
def verify_weights(distribution):
    epsilon = 0.000000001 # allow small numerical error
    sum = 0.0
    for item in distribution:
        sum += item[1]
    assert abs(sum - 1.0) < epsilon

# This method is slow but simple
def random_select(distribution):
    r = random.random()
    sum = 0.0
    for item in distribution:
        sum += item[1]
        if sum > r:
            return item
    return distribution[-1] # some numerical error, return last element

drinks = [("Coffee", 0.3), ("Tea", 0.2), ("OJ", 0.4), ("Milk", 0.07), ("RootBeer", 0.03)]
verify_weights(drinks)
count = {drink: 0 for drink in drinks}

numTries = 100
for i in range(numTries):
    names = [name[0] for name in drinks ]
    w = (30,20,40,7,3)
    prob = (0.3,0.2,0.4,0.07,0.03)
    drink = random_select(drinks)
    d = random.choices(names,weights=w,k=1)[0]
    #drink = (d,prob[names.index(d)])
    #print(drink)
    #print("Experiment {}: {}".format(i, drink[0]))
    count[drink] += 1
    
for drink in drinks:
    print("{} probability {}, empirical frequency {}".format(
            drink[0], drink[1], count[drink] / numTries))
