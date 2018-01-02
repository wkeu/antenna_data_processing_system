# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:29:16 2017

@author: matt.slevin
"""

fig, ax = plt.subplots(figsize=[13,7])
#make room
plt.subplots_adjust(left=0.25, bottom=0.25)

axcolor = 'lightgoldenrodyellow'

az_co=all_ports["P1"]["AZ T0 CO"]["amplitude"]
az_cr=all_ports["P1"]["AZ T0 CR"]["amplitude"]
az_co=az_co.convert_objects(convert_numeric=True)
az_cr=az_cr.convert_objects(convert_numeric=True )                           

co,cr = normalise2(az_co,az_cr)

keys=tuple(co.keys())

x = np.arange(0,360)

s1 = co["3300.00"]
s2 = cr["3300.00"]

l1,= plt.plot(x, s1, lw=1,alpha=0.8, color='red')
l2,= plt.plot(x, s2, lw=1,alpha=0.8, color='red')
plt.axis([0, 360, -50, 0])
plt.grid(True,alpha=0.5)
