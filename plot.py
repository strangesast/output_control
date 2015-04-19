import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def get_voltage(volt):
    return volt

def set_voltage(volt):
    f = volt
    return f

def logic(volt, target):
    v = get_voltage(volt)

    if v < target:
        n = v + 1
    else:
        n = v - 1

    return set_voltage(n)


target = 10
def data_gen():
    t = data_gen.t
    #t = time.time()
    ti = time.time()
    f = 0 
    cnt = 0
    while cnt < 1000:
        cnt+=1

        f = logic(f, target)
        print(f)

        #f = np.sin(2*np.pi*t) * np.exp(-t/10.)

        t = time.time() - ti
        b = (t, f)
        yield b

data_gen.t = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 20)
ax.set_xlim(0, 1)
ax.grid()
xdata, ydata = [], []

f = 0

def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
    repeat=False)

plt.show()


"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_line(num, data, line):
    line.set_data(data[...,:num])
    return line,

fig1 = plt.figure()

data = np.random.rand(2, 25)
l, = plt.plot([], [], 'r-')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
    interval=50, blit=True)
#line_ani.save('lines.mp4')

fig2 = plt.figure()

x = np.arange(-9, 10)
y = np.arange(-9, 10).reshape(-1, 1)
base = np.hypot(x, y)
ims = []
for add in np.arange(15):
    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
    blit=True)
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

plt.show()
"""
