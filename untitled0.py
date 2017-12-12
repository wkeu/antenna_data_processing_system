# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:32:28 2017

@author: MJ.McAssey
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.random((4,3)), columns=list('CD'))
for col in ('C', 'D'):
    df[col].plot(legend=True)
plt.show()