import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import redis

redisClient = redis.StrictRedis(host='192.168.0.87', port=6379, db=0)

plt.axis([0, 2, -90, 90])
time = 0
while(True):
    y = float(redisClient.get('pitch'))
    plt.scatter(time, y)
    plt.pause(0.05)
    sleep(0.1)
    time += 0.01
    plt.axis([0, 2 + time, -90, 90])

plt.show()