# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:29:26 2017

@author: MJ.McAssey
"""

import pylab as plt

x = [0, 1, 2, 3, 4]
y = [ [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [9, 8, 7, 6, 5] ]
labels=['foo', 'bar', 'baz']
colors=['r','g','b']
headers = list(y.dtypes.index)

# loop over data, labels and colors
for i in range(len(y)):
    plt.plot(x,y[i],'o-',color=colors[i],label=labels[i])

plt.legend()
plt.show()
