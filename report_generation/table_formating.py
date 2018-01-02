# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:35:04 2017

@author: matt.slevin
"""

"""
Example code showing how to implement pivot tables. This could be usefull for
creating a function which allows for the automatic generation of tables 
"""


from __future__ import print_function
import pandas as pd
import numpy as np


df = pd.read_excel("sales_funnel.xlsx")
df.head()

#Pivot the data to summarize
sales_report = pd.pivot_table(df, index=["Manager", "Rep", "Product"], values=["Price", "Quantity"],
                           aggfunc=[np.sum, np.mean], fill_value=0)
sales_report.head()

# Generate some overall descriptive statistics about the entire data set. In 
# this case, we want to show the average quantity and price for CPU and Software
# sales.

print(df[df["Product"]=="CPU"]["Quantity"].mean())
print(df[df["Product"]=="CPU"]["Price"].mean())
print(df[df["Product"]=="Software"]["Quantity"].mean())
print(df[df["Product"]=="Software"]["Price"].mean())

#From this point we can copy and paste the data into an excel spreadsheet if we 
#wish 

###############################################################################
#
# HTML
#
###############################################################################
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")

template_vars = {"title" : "Sales Funnel Report - National",
                 "national_pivot_table": sales_report.to_html()}

html_out = template.render(template_vars)

# to save the results
with open("my_new_file.html", "wb") as fh:
    fh.write(html_out)

###############################################################################
#
#   Templating
#
###############################################################################

