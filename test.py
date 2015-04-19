import time
import random
import matplotlib.pyplot as plt
import numpy as np

initial_voltage = 0
# output maximums.  should be instead read from config.json
max_v = 10
min_v = 0

def wait(old, new):
    """ wait time (before changing voltage again) corresponds to 
        function of change in v
    """
    fac = 1 # wait n times longer than delta_v

    delta_v = abs(new - old)

    return delta_v*fac


def voltage_set(volt):
    """ set device output voltage
    """
    last = voltage_set.last
    current = volt # (global) last set value

    suggested_wait = wait(last, volt)

    voltage_set.last = volt

    # do set operation

    return suggested_wait


def voltage_read(c):
    """ get analog voltage from device
    """

    v = c + (-0.5 + random.random())
    return v


target = 10 # target voltage

keep = 50 # how many to keep in lib
lib = []
current = 0


# initialize stuff
voltage_set.last = initial_voltage
init = time.time()
n = init
y = initial_voltage


# plotting
def xory(l, o):
    return [x[o] for x in l]

plt.ion() # turn on interactive plotting

fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = fig.add_subplot(111)
ax2.plot([0, 10*10], [target, target], 'k-')
plt.ylim([0, target + target*0.1])

line1, = ax.plot(xory(lib, 0), xory(lib, 1), 'ro')


while y < target + 0.8:
    i = time.time()
    v = voltage_read(y)
    lib.append((i-init, v))
    lib = lib[-keep:]
    lower = min(xory(lib, 0))

    plt.xlim([lower, i-init]) # move with the data

    line1.set_xdata(xory(lib, 0))
    line1.set_ydata(xory(lib, 1))
    fig.canvas.draw()

    # save frame
    fig.savefig("./png/{}.png".format(str(i)))
    

    if i > n:
        w = voltage_set(y)
        y+=1
        n = time.time() + w


time.sleep(10)
