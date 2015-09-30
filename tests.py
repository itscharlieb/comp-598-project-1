import numpy as np
from learner import *

path = "./OnlineNewsPopularity/OnlineNewsPopularity.csv"
data = readData(path)

values = train(gradientDescent, data)
print values