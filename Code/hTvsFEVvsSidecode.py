# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 16:32:50 2025 changed OB 06-05-2026

@author: Natasha Pickard
"""
import pandas as pd
import matplotlib.pyplot as plt
import os.path

plt.rcParams['axes.grid']=False
plt.rcParams["figure.figsize"] = [8,6]
plt.rcParams['axes.edgecolor']='black'
fig, ax1 = plt.subplots()

# Import the Data
central_path = "/Users/onnobokhove/miniforge3/floodsMATH3001main/Data/"
nch = 1
if nch==0:
    Data = pd.read_csv(r'C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Aire Armley 2015 hT FEV and Sidelength.csv')
else:
    Data = pd.read_csv(r'/Users/onnobokhove/miniforge3/floodsMATH3001main/Data/Aire Armley 2015 hT FEV and Sidelength.csv')
#Aire 2015: C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Aire Armley 2015 hT FEV and Sidelength.csv
#Don 2005: C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Don Hadfields 2007 hT FEV and Sidelength.csv
hT = Data['hT']
FEV = Data['FEV']
Side = Data['Side']

ax1.set_xlabel('$h_T$ [m]', size=15)
ax1.set_ylabel('$FEV$ [Mm$^3$]', size=15, color='tomato')
ax1.plot(hT, FEV, color='tomato', marker='x', markeredgecolor='k')
ax1.tick_params(axis='y', labelcolor='tomato')
ax1.set_ybound(0,31)
ax1.set_ylim(0,31)
ax1.set_xlim(2.4,5.3)


ax2 = ax1.twinx()

ax2.set_ylabel('2m deep square lake side length [m]', size=15, color='cornflowerblue')
ax2.plot(hT, Side, color='cornflowerblue', marker='o', markeredgecolor='k')
ax2.tick_params(axis='y', labelcolor='cornflowerblue')
ax2.set_ybound(0,4500)


fig.tight_layout()

save_figure=True
figure_name= f"hTvsFEVside.pdf"
data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)
    
if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()
