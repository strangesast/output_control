import time
import random
import matplotlib.pyplot as plt
import numpy as np
import math

initial_voltage = 0
# output maximums.  should be instead read from config.json
max_v = 10
min_v = 0

def wait(old, new):
    """ wait time (before changing voltage again) corresponds to 
        function of change in v
    """
    w_fac = 1 # wait n times longer than delta_v

    delta_v = abs(new - old)

    return delta_v*w_fac


def voltage_set(volt):
    """ set device output voltage
    """
    last = voltage_set.last
    current = volt # (global) last set value

    suggested_wait = wait(last, volt)

    voltage_set.last = volt

    # do set operation

    print(volt)
    return suggested_wait


def voltage_read(c):
    """ get analog voltage from device
    """

    v = c + (-0.5 + random.random()) # basic linear

    scale = 10 # approach this, must be greater than target
    v = scale*(1 - math.exp(-c))
    #print(v)
    return v


def weighted(both):
    """ accepts lib array
    """

    ts = [x[0] for x in both] # t over lib
    dts = [j-i for i, j in zip(ts[:-1], ts[1:])] # change in t

    vs = [x[1] for x in both] # v over lib
    dvs = [j-i for i, j in zip(vs[:-1], vs[1:])] # change in v

    ms = [v/t for v, t in zip(dvs, dts)] # slope

    weight = [(1/x**2)/fac if x != 0 else 1/fac for x in range(len(ms))][::-1] # reverse


    appl = [i*j for i, j in zip(ms, weight)]



    l = len(ms) if len(ms) != 0 else 1

    return sum(appl)


target = 5 # target voltage
slow = 0.005 # how fast do you approach the target

keep = 50 # how many to keep in lib
fac = sum([x**-2 if x != 0 else 1 for x in range(keep)]) # scale weight

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

line2, = ax.plot([0, 0], [0, 0], 'b-')


framecount = 0
while y < target + 0.8:
    framecount+=1
    i = time.time()

    v = voltage_read(y)
    lib.append((i-init, v))
    lib = lib[-keep:]
    lower = min(xory(lib, 0))

    m = weighted(lib)
    if(m == 0):  # this should never be exactly 0
        m = 1

    plt.xlim([lower, i-init]) # move with the data
    plt.ylim([0, max([1.1*target, max(xory(lib, 1))])]) # move with the data

    line1.set_xdata(xory(lib, 0))
    line1.set_ydata(xory(lib, 1))

    # plot slope
    line2.set_xdata([lower, i-init])
    line2.set_ydata([0, (i-init-lower)*m])

    fig.canvas.draw()

    # save frame
    text = ('000' + str(framecount))[-3:]
    fig.savefig("./png/{}.png".format(text))
    
    delta_y = (target - v)/m*slow

    if abs(delta_y) < 0.001:
        break

    if i > n:
        w = voltage_set(y)
        if v < target:
            y+=delta_y
        else: 
            y+=delta_y

        n = time.time() + w


time.sleep(100)
