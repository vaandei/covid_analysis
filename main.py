#=======================================================================================#
import sys
import os
import csv
import numpy as np
import scipy as sp
import matplotlib
#matplotlib.use('Agg') 
from matplotlib import pyplot as plt
from decimal import Decimal
import multiprocessing as mp
from itertools import repeat

import plots as pl
import tools as tl
#=======================================================================================#

confirmed_data = []
death_data = []
recovery_data = []
tl.get_data([confirmed_data,death_data,recovery_data])

sizer = np.shape(confirmed_data) ; print(sizer)
#print(confirmed_data[0])

# sort by countries
country_list = []
for i in range(1,sizer[0]):
    namer = confirmed_data[i][1]
    if namer not in country_list:
        country_list.append(namer)

print(np.size(country_list))
print(country_list)
num_countries = np.size(country_list)
country_rates = np.zeros((num_countries,sizer[1]-4))
for i in range(num_countries):
    for j in range(1,sizer[0]):
        if country_list[i] == confirmed_data[j][1]:
            for k in range(4,sizer[1]):
                country_rates[i,k-4] += float(confirmed_data[j][k])

wanted = ["China","US","Italy","Germany","Korea, South"]  # ["Italy","US","Germany","Korea, South"]  
wanted_pop = [1401710720.,329431067.,60252824.,83149300.,51780579.]
wanted_pop_density = [418.,200.,200.,233.,517.]

# actual China pop density 145, but will use an average of south, east and central
# actual US pop density 34, but will use number for city pop density


fig, ax = plt.subplots()
for i in range(num_countries):
    #if country_rates[i,-1] > 800:
    if country_list[i] in wanted:
        num = wanted.index(country_list[i])
        #fig, ax = plt.subplots()
        legend = country_list[i]
        if 1==0:  # actual dates
            x = np.array(range(sizer[1]-4)) ; print(np.size(x)) ; x = np.ma.masked_equal(x,0.0) ; print(np.size(x))
            y = np.array(country_rates[i,:]) ; y = np.ma.masked_equal(y,0.0)
        if 1==1: # shift time to where day 0 has > 100 confirmed cases
            for j in range(np.size(country_rates[i,:])):
                if country_rates[i,j] > 200.:
                    val = j
                    break
            x = np.array(range(np.size(country_rates[i,:])-j)) ; y = np.array(country_rates[i,j:])
        pl.scatter_plot(x,(y),['Confirmed Cases','Days','Num Affected',legend],'.')
        #pl.scatter_fit_plot(pl.logistic,(x),(y),['Confirmed Cases','Days','Num Affected (log10)',legend])
        #pl.scatter_fit_plot(pl.logistic,(x),(y)/wanted_pop_density[num],['Confirmed Cases','Days','Num Affected per Population Density',legend])
        popt = tl.fit_function(pl.logistic,x,y/wanted_pop_density[num],legend)
        num_sim = 60
        modelPredictions = pl.logistic((range(num_sim)), *popt)
        #pl.scatter_plot(range(num_sim),modelPredictions,['Confirmed Cases','Days','Num Affected',legend],'-')
        pl.scatter_plot(range(num_sim),modelPredictions*wanted_pop_density[num],['Confirmed Cases','Days','Num Affected',legend],'-')

        #x = np.array(range(sizer[1]-4)) ;  trim_size = np.size(np.trim_zeros(x)) ; x = x[:trim_size]
        #y = np.array(country_rates[i,:]) ; print(y) ; y = y[np.size(y)-trim_size:] ; print(y)

plt.show()


if 1==0:
    fig, ax = plt.subplots()
    for i in range(sizer[0]):
        if confirmed_data[i][1] =='US':
            vals = np.array([int(i) for i in confirmed_data[i][4:]])
            legend = str(confirmed_data[i][0])+','+str(confirmed_data[i][1])
            pl.scatter_plot(range(sizer[1]-4),vals,['Confirmed Cases','Days','Num Affected',legend])

    plt.show()
num = 0
for i in range(sizer[0]):
    if confirmed_data[i][1] =='US':
        num += 1
        #print(confirmed_data[i][0],confirmed_data[i][0][1])