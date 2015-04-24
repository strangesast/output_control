import time
import random
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
    w_fac = 0.01 # wait n times longer than delta_v

    delta_v = abs(new - old)

    return delta_v*w_fac


def voltage_set(volt):
    volt = max(min(volt, max_v), min_v)
    """ set device output voltage
    """
    last = voltage_set.last
    current = volt # (global) last set value

    suggested_wait = wait(last, volt)

    voltage_set.last = volt

    # do set operation

    print("wait: {}".format(suggested_wait))
    return suggested_wait


def voltage_read(c):
    """ get analog voltage from device
    """

    _voltage = 10*c + 1/2*(-0.5 + random.random()) # basic linear
    scale = 10 # approach this, must be greater than target
    #_voltage = scale*(1 - math.exp(-c))
    #_voltage = scale*math.sin(c)*math.exp(c) - 0.2*(0.5 + random.random())

    return _voltage


def slope():
    """ what input_voltage corresponds to what response_voltage
    """

    d = [x / y for x, y in zip(reads[:-1], writes)]

    print("slope: {}".format(sum(d) / len(d) if len(d) > 0 else 1))
    return sum(d) / len(d) if len(d) > 0 else slope_guess


def fluc_target(_time):
    """ change target over time
    """
    
    period = 1/100
    return 9 + 1*(1/2 + 1/2*math.sin(period*_time))


target = 9 # target voltage
slow = 0.5 # how fast do you approach the target

keep = 50 # how many to keep to assess the slope
fac = sum([x**-2 if x != 0 else 1 for x in range(keep)]) # scale weight

lib = []
current = 0
slope_guess = 1


# initialize stuff
voltage_set.last = initial_voltage
init_time = time.time()
next_time = init_time
input_voltage = initial_voltage

plot = False
savefig = False

def xory(l, o):
    return [x[o] for x in l]

if plot:
    import matplotlib.pyplot as plt
    plt.ion() # turn on interactive plotting
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    target_plot, = ax.plot([0, 10*10], [target, target], 'k-')
    
    line1, = ax.plot(xory(lib, 0), xory(lib, 1), 'ro')
    
    line2, = ax.plot([0, 0], [0, 0], 'b-')
    
    plt.ylim([0, target + target*0.1])

framecount = 0
delta_input_voltage = 0

reads = []   # response voltage history
writes = []  # input voltage history
changes = [] # delta_input_voltage history

while True:
    framecount+=1

    current_time = time.time()
    time_post_init = current_time - init_time

    #target = fluc_target(current_time) # get target output_voltage
    target = 10

    response_voltage = voltage_read(input_voltage)

    lib.append((time_post_init, response_voltage))
    lib = lib[-keep:]

    if len(lib[:-4]) > 3:
        vs = [x[1] for x in lib[:-4]]
        avg = sum(vs) / len(vs)
        o = [ x - avg for x in vs]
        b = sum(o) / len(o)
        if b < 0.01: next_time = time.time() - 1000
        

    #print(sum(d)/len(d) if len(d) > 0 else 1)

    change = [(lib[i+1][1] - elem[1])/(lib[i+1][0] - elem[0]) for i, elem in enumerate(lib[:-1])]

    # plot target
    if plot:
        lower = min(xory(lib, 0))

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


        #text = ('000' + str(framecount))[-3:]
        # save frame
        if savefig:
            fig.savefig("./png/{}.png".format(text))
    

    if current_time > next_time:
        print('changing voltage')
        time.sleep(1)
        reads.append(response_voltage)
        reads = reads[-keep:]

        m = slope()
        delta_input_voltage = (target - response_voltage)/m*slow if m > 0.1 else 0.01

        changes.append(delta_input_voltage)
        changes = changes[-10:]

        # if average change is small for a while, break
        if sum(changes) / len(changes) < 0.01: break

        wait_time = voltage_set(input_voltage)
        next_time = time.time() + wait_time

        input_voltage += delta_input_voltage

        writes.append(input_voltage)
        writes = writes[-keep:]



time.sleep(100)
