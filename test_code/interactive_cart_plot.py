import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons



az_co=all_ports["P1"]["AZ T0 CO"]["amplitude"]
az_cr=all_ports["P1"]["AZ T0 CR"]["amplitude"]
az_co=az_co.convert_objects(convert_numeric=True)
az_cr=az_cr.convert_objects(convert_numeric=True )                           
  
fig, ax = plt.subplots(figsize=[13,7])
#make room
plt.subplots_adjust(left=0.25, bottom=0.25)

axcolor = 'white'
  
co,cr = normalise2(az_co,az_cr)

keys=tuple(co.keys())

x = np.arange(0,360)

s1 = co["3300.00"]
s2 = cr["3300.00"]

l1,= plt.plot(x, s1, lw=1,alpha=0.7, color='red')
l2,= plt.plot(x, s2, lw=1,alpha=0.7, color='red')

plt.axis([0, 360, -50, 0])
plt.grid(True,alpha=0.5)

x_tick_spacing = 20
y_tick_spacing = 3
ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))

rax = plt.axes([0.025, 0.01, 0.125, 0.95], facecolor=axcolor, frameon=True)
radio = RadioButtons(rax,keys , active=0)
for circle in radio.circles: # adjust radius here. The default is 0.05
    circle.set_radius(0.018)


def wave_sel_func(label):
    l1.set_ydata(cr[label])
    l2.set_ydata(co[label])
    fig.canvas.draw_idle()
radio.on_clicked(wave_sel_func)

#
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

plt.show()
