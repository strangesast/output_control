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

    #print(volt)
    return suggested_wait


def voltage_read(c):
    """ get analog voltage from device
    """

    _voltage = 10*c + 1/2*(-0.5 + random.random()) # basic linear
    scale = 10 # approach this, must be greater than target
    #_voltage = scale*(1 - math.exp(-c))
    _voltage = scale*math.sin(c)*math.exp(c) - 0.2*(0.5 + random.random())

    return _voltage


def weighted(both):
    """ accepts lib array
    """

    # needs to be m = delta_v / delta_y
    # rather than m = delta_v / delta_t
    # probably can be done mostly in lib (both)

    ts = [x[0] for x in both] # t over lib
    dts = [j-i for i, j in zip(ts[:-1], ts[1:])] # change in t

    vs = [x[1] for x in both] # v over lib
    dvs = [j-i for i, j in zip(vs[:-1], vs[1:])] # change in v

    ms = [v/t for v, t in zip(dvs, dts)] # slope

    m_bar = sum(ms)/len(ms) if len(ms) > 0 else 0.01
    delta_m = [i - m_bar for i in ms]

    #weighted_m = [m_bar + dm*math.exp(-dm**2) for dm in delta_m]
    #weighted_m = sum(weighted_m)/len(weighted_m)

    weight = [(1/x**2)/fac if x != 0 else 1/fac for x in range(len(ms))][::-1] # reverse


    appl = [i*j for i, j in zip(ms, weight)]



    l = len(ms) if len(ms) != 0 else 1


    # should always be positive, not sure why ever returning neg
    #weighted_m = abs(sum(appl))
    weighted_m = abs(sum(ms))/l if abs(sum(ms))/l > 0.01 else 0

    return weighted_m


def fluc_target(_time):
    """ change target over time
    """
    
    period = 1/100
    return 9 + 1*(1/2 + 1/2*math.sin(period*_time))


target = 9 # target voltage
slow = 0.01 # how fast do you approach the target

keep = 50 # how many to keep in lib
fac = sum([x**-2 if x != 0 else 1 for x in range(keep)]) # scale weight

lib = []
current = 0


# initialize stuff
voltage_set.last = initial_voltage
init_time = time.time()
next_time = init_time
input_voltage = initial_voltage

# plotting
def xory(l, o):
    return [x[o] for x in l]

plt.ion() # turn on interactive plotting

fig = plt.figure()
ax = fig.add_subplot(111)

target_plot, = ax.plot([0, 10*10], [target, target], 'k-')

line1, = ax.plot(xory(lib, 0), xory(lib, 1), 'ro')

line2, = ax.plot([0, 0], [0, 0], 'b-')

plt.ylim([0, target + target*0.1])

framecount = 0
delta_y = 0
m = 1

#while input_voltage < target + 0.8:
while True:
    framecount+=1
    current_time = time.time()

    target = fluc_target(current_time)
    response_voltage = voltage_read(input_voltage)

    # (time_since_init)
    time_post_init = current_time - init_time
    lib.append((current_time-init_time, response_voltage))
    lib = lib[-keep:]
    lower = min(xory(lib, 0))


    delta_y = (target - response_voltage)/m*slow if m > 0.1 else 0.01

    m = weighted(lib)

    # plot target
    target_plot.set_xdata([lower, current_time - init_time])
    target_plot.set_ydata([target, target])

    plt.xlim([lower, current_time-init_time]) # move with the data
    #plt.ylim([0, max([1.1*target, max(xory(lib, 1))])]) # move with the data

    line1.set_xdata(xory(lib, 0))
    line1.set_ydata(xory(lib, 1))

    # plot slope
    #line2.set_xdata([lower, current_time-init_time])
    #line2.set_ydata([0, (current_time-init_time-lower)*m])

    fig.canvas.draw()

    # save frame
    #text = ('000' + str(framecount))[-3:]
    #fig.savefig("./png/{}.png".format(text))
    

    #print(target - response_voltage)
    #print(m)

    if abs(delta_y) < 0.001:
        pass
        #break
        #print(target)

    if current_time > next_time:
        wait_time = voltage_set(input_voltage)
        if response_voltage < target:
            input_voltage+=delta_y
        else: 
            input_voltage+=delta_y

        next_time = time.time() + wait_time


time.sleep(100)
