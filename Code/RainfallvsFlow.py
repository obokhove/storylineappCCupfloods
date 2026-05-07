# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 05:56:04 2025

@author: Natasha Pickard Changed OB 06-05-2026
"""

import matplotlib.pyplot as plt
import pandas as pd
import os.path
import matplotlib.dates as mdates

# --- Load the data ---
# If reading from CSV, replace this with your file path:
# df = pd.read_csv("yourfile.csv")
# If data is already in memory, skip to parsing

# Parse your structured data
# Assuming columns: date, value (rainfall), Flow

# Define your file mapping
central_path = "/Users/onnobokhove/miniforge3/floodsMATH3001main/Data/"
nch = 1
if nch==0:
    df = pd.read_csv(r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\2015 Rainfall Lower Laithe 2 weeks.csv")
else:
    df = pd.read_csv(r"/Users/onnobokhove/miniforge3/floodsMATH3001main/Data/2015 Rainfall Lower Laithe 2 weeks.csv")
        

#2015 2 weeks: "C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\2015 Rainfall Lower Laithe 2 weeks.csv"
#2015 flood: C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\2015 Rainfall Lower Laithe Bradford.csv

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df.set_index('date', inplace=True)

# Resample to daily: sum rainfall, average flow
df_daily = pd.DataFrame()
df_daily['Rainfall'] = df['value'].resample('D').sum()
df_daily['Flow'] = df['Flow'].resample('D').mean()

# --- Plotting ---
fig, ax1 = plt.subplots(figsize=(14, 6))

# Rainfall as bar plot
ax1.bar(df_daily.index, df_daily['Rainfall'], width=0.8, color='skyblue', label='Rainfall [mm]')
ax1.set_ylabel('Rainfall [mm]', fontsize=16 )
ax1.set_xlabel('Date', fontsize=16)

# X-axis formatting
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.xticks(rotation=45)

# Flow as line plot (right axis)
ax2 = ax1.twinx()
ax2.plot(df_daily.index, df_daily['Flow'], color='black', linewidth=2, label='Flow [m³/s]')
ax2.set_ylabel('Flow [m³/s]', fontsize=14)

ax1.tick_params(axis='both', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)

plt.tight_layout()

save_figure=True
figure_name= f"rainfall.pdf"
data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)
    
if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()
