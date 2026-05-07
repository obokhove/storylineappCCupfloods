
"""
Created on Mon Mar 31 22:28:21 2025/OB: 11-03-2026 vv
@author: Natasha Pickard, built on Zheming Zhang's code, update by Onno Bokhove 11-03-2026 vv
"""
#This code is taken from Zheming Zhang and rivertestgen which can be found at:
#https://github.com/Flood-Excess-Volume/RiverDon/tree/master/Pythoncode
#and at
#https://github.com/Flood-Excess-Volume/RiverDon/tree/master/Integratedcode
#this code along with the Teme data was used to produce the graph relating to the River Teme FEV

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import bisect
import os.path
from mpl_toolkits.mplot3d import Axes3D
fig, ax = plt.subplots()

#Import the data from a csv file. In this case I import my River Teme data
#data must have 3 columns with headings 'Time', 'Height', 'Flow'
#and note that this code will only work successfuly for data where there is
#one single peak

# Define your file mapping;11-03-2026 OB directory choice; make your own
# Central directory, set it:
central_path = "/Users/onnobokhove/miniforge3/floodsMATH3001main/Data/"
nch = 1
if nch==0:
    file_paths = {
        "Armley_2015": r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Rotherham Don 2007.csv",
        "Armley_2020": r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Aire Armley 2020 Stage and Flow.csv",
        "Armley_2022": r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Aire Armley 2022 Stage and Flow.csv",
        "Don_Tesco_2007": r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Rotherham Don 2007.csv",
        "Don_Hadfields_2007": r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Don Hadfields 2007 Stage and Flow.csv"
    }
elif nch==1:
    file_namess = {
        "Armley_2015": "Aire Armley 2015 Stage and Flow.csv",
        "Armley_2020": "Aire Armley 2020 Stage and Flow.csv",
        "Armley_2022": "Aire Armley 2022 Stage and Flow.csv",
        "Don_Tesco_2007": "Rotherham Don 2007.csv",
        "Don_Hadfields_2007": "Don Hadfields 2007 Stage and Flow.csv"
    }
    file_paths = {k: os.path.join(central_path, v) for k, v in file_namess.items()}
    
# Set which file to load, e.g. selected_file = "Don_Tesco_2007"
selected_file = "Armley_2015"
selected_file = "Armley_2020"

# Load the CSV
Data = pd.read_csv(file_paths[selected_file])

# Automatically set threshold height 'h' based on the selected file
if selected_file == "Armley_2015":
    ht = 3.9 # Trial and 56 errors by hand ht = 3.9 normal; WRONG/OLD for FEVrest=[0.7,1.26] ht = [4.983,4.78]; new OB  ht=[4.886,4.78] QT_GRR=[320.98,310.12] FEVGRR = [699539.37,1264513.73]
    error = 0.055
    startdate = 24
elif selected_file == "Armley_2020":
    ht = 3.9 # Trial and errors by hand ht = 3.9 normal; ht = 
    error=0.055
    startdate=8
elif selected_file == "Armley_2022":
    ht = 3.9
    error=0.055
    startdate=19
elif selected_file == "Don_Tesco_2007":
    ht = 1.9
    error=0.08
    startdate=24
elif selected_file == "Don_Hadfields_2007":
    ht = 2.9
    error=0.08
    startdate=24
else:
    raise ValueError("Threshold height for selected file is not defined.")

# Optional: print for confirmation
print(f"Loaded {selected_file} with threshold height h = {ht} m")

time=Data['Time']
height=Data['Height']
flow=Data['Flow']
height1=height[height>ht]
hm=np.mean(height1)
startdate=startdate
print(max(height))
print(hm)

plt.rcParams["figure.figsize"] = [11,8]
plt.rcParams['axes.edgecolor']='white'
ax.spines['left'].set_position(('zero'))
ax.spines['bottom'].set_position(('zero'))
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

time_increment=(time[1]-time[0])*24*3600

number_of_days=int((len(time)*(time[1]-time[0])))

def scale(x):
    return ((x-min(x))/(max(x)-min(x)))

def scale0(x):
    return ((x-0.0*min(x))/(max(x)-0.0*min(x)))

error_height_up = [i * (1+error) for i in height]
error_height_down = [i * (1-error) for i in height]
scaledtime=scale(time)
faac = 0 # OB: start height and flow at 0 or min's of flow and height data
if faac==1:
    # OB old:
    scaledheight=scale(height)
    scaledFlow=scale(flow)
elif faac==0:
    scaledheight=scale0(height)
    scaledFlow=scale0(flow)
hup=ht*(1+error)
print(hup)

# Here we calculate qt, qtmin and, qtmax 
# This code was taken from rivertestgen
qt = 0
nwin = 0
for i in range(1,len(height)):
        if height[i] > ht and height[i-1] < ht and nwin==0:
            qt =  flow[i-1]+(flow[i]-flow[i-1])*(ht-height[i-1])/(height[i]-height[i-1])
            nwin = 1
        if height[i] < ht and height[i-1] > ht and nwin==0:
            qt =  flow[i-1]+(flow[i]-flow[i-1])*(ht-height[i-1])/(height[i]-height[i-1])
            nwin = 1
qtmin = (1.0-error)*qt
qtmax = (1.0+error)*qt

scaledFlow_up = [i*(1+error) for i in scaledFlow]
scaledFlow_down = [i*(1-error) for i in scaledFlow]
negheight=-scaledheight
negday=-(scaledtime)

# Now the 4 quadrant graph is plotted

ax.plot(negheight,scaledFlow,'black',linestyle='--',linewidth=2)
ax.plot([0,-1],[0,1],'blue',linestyle='--',marker='',linewidth=2)
ax.plot(scaledtime, scaledFlow,'black',linewidth=2)
ax.plot(negheight, negday,'black',linewidth=2)

maxfl = max(flow)
# OB old: minhe = min(height)
# OB old: minfl = 0.0*min(flow)
minfl = faac*min(flow)
minhe = faac*min(height)
maxhe = max(height)

scaledht = (ht-minhe)/(maxhe-minhe)
scaledqt = (qt-minfl)/(maxfl-minfl)

# OB: add check on rating curve; parameters for limbs
h0, h1, h2, h3 = 0.156, 0.685, 1.917, 4.17
c1, a1, b1 = 30.69, 0.156, 1.115
c2, a2, b2 = 27.884, 0.028, 1.462
c3, a3, b3 = 30.127, 0.153, 1.502
hhmin = h0
hhmax = maxhe
Nhh = 1000
hhh = np.linspace(hhmin,hhmax,Nhh)
mask1 = ((hhh > h0) & (hhh <= h1)).astype(float)
mask2 = ((hhh > h1) & (hhh <= h2)).astype(float)
mask3 = ((hhh > h2)).astype(float) # mask3 = ((hhh > h2) & (hhh <= h3)).astype(float)
qqq = mask1*c1*(hhh-a1)**b1 + mask2*c2*(hhh-a2)**b2 + mask3*c3*(hhh-a3)**b3 # 1st limb between h0<hh<h1, h1<hh<h2, hh>h2.
np.savetxt("data/hh_qqqrtnormal.txt", np.column_stack((hhh, qqq)), header="hh qqq",  fmt="%.10f")
scaledhht = (hhh-minhe)/(maxhe-minhe)
scaledqqt = (qqq-minfl)/(maxfl-minfl)
negscaledhht = -scaledhht
ax.plot(negscaledhht,scaledqqt,'black',linestyle='-',linewidth=1)
# OB: now check plotting the inverse since that is needed for climate-change uplift
q0 = c1*(h0-a1)**b1 # 1st limb between h0<hh<h1,
q1 = c1*(h1-a1)**b1 # 1st limb between h0<hh<h1
q2 = c2*(h2-a2)**b2 # 2nd limb between h1<hh<h2
q3 = c3*(h3-a3)**b3 # 3rd limb between hh>h3.
qmask1 = ((qqq > q0) & (qqq <= q1)).astype(float)
qmask2 = ((qqq > q1) & (qqq <= q2)).astype(float)
qmask3 = ((qqq > q2)).astype(float) #
print('q0:',q0,'q1',q1,'q2',q2,'q3',q3)
hhh2 = qmask1*(a1+(qqq/c1)**(1/b1))+qmask2*(a2+(qqq/c2)**(1/b2))+qmask3*(a3+(qqq/c3)**(1/b3))
scaledhht2 = (hhh2-minhe)/(maxhe-minhe)
negscaledhht2= -scaledhht2
ax.plot(negscaledhht2,scaledqqt,'green',linestyle=':',linewidth=1)
#
# GRR rating curve, plot in quadrant 2;
# a) Put in h_T to obtain a new Q_TGRR; then calculated new FEV_GRR with new Q_TGRR
# c) Then for S0 subtract V_AFPC to find new FEV_GRR+AFPC,
# b) plot new rating curve
# d) then shoot hT's to find new hT_GRR+AFPC to protect against hmax=5.22 flood
# Then add 0.13m to get actual wall height relative to river gauge
Slope0, bankslope, Cmanning, wGRR, hGRR = 0.0005, 2, 0.04, 5, 1.9
if ht < hGRR:
    qtGRR = qt
elif ht >= hGRR:
    qtGRR = qt+(np.sqrt(Slope0)/Cmanning)*((ht-hGRR)*wGRR)**(5/3)/(wGRR+(ht-hGRR)*np.sqrt(1+bankslope**2))**(2/3) # a) For h>hGRR

qtminGRR = qtGRR*(1-error)
qtmaxGRR = qtGRR*(1+error)                                                
# b) From rivertestgen FEVGRR calculation; recall flow stays same; h changes to hGRR
FlowminGRR = (1.0-error)*flow
FlowmaxGRR = (1.0+error)*flow
FlowGRR = []
for i in flow:
    if i>=qtGRR:
        FlowGRR.append((i-qtGRR)*(time_increment))
flowminGRR = []
for i in FlowminGRR:
    if i >= qtminGRR: # OB 
        flowminGRR.append((i - qtminGRR) * (time_increment)) # OB 
flowmaxGRR = []
for i in FlowmaxGRR:
    if i >= qtmaxGRR: # OB 
        flowmaxGRR.append((i - qtmaxGRR) * (time_increment)) # OB 
FEVGRR = sum(FlowGRR)
FEVGRR_max = sum(flowmaxGRR)
FEVGRR_min = sum(flowminGRR)
print(f"Q_GRR: {qtGRR:.2f}, [{qtminGRR:.2f},{qtmaxGRR:.2f}]")
print(f"FEV_GRR = {FEVGRR:.2f} in [{FEVGRR_min:.2f}, {FEVGRR_max:.2f}]")
# c_ ready for plotting QGRR(h)

maskGRR =  (hhh > hGRR).astype(float)
qqqGRR = qqq + maskGRR*(np.sqrt(Slope0)/Cmanning)*((hhh-hGRR)*wGRR)**(5/3)/(wGRR+(hhh-hGRR)*np.sqrt(1+bankslope**2))**(2/3) # a)
scaledqqtGRR = (qqqGRR-minfl)/(maxfl-minfl)
np.savetxt("data/hh_qqqrtGRR.txt", np.column_stack((hhh, qqqGRR)), header="hh qqqGRR",  fmt="%.10f")
ax.plot(negscaledhht2,scaledqqtGRR,'blue',linestyle='-.',linewidth=2)


QT=[]
for i in scaledFlow:
    i = scaledqt
    QT.append(i)

SF=np.array(scaledFlow)
e=np.array(QT)
    
ax.fill_between(scaledtime,SF,e,where=SF>=e,facecolor='blue')

idx = np.argwhere(np.diff(np.sign(SF - e))).flatten()

f=scaledtime[idx[0]]
print(f)
g=scaledtime[idx[-1]]
print(g)

def unscaletime(x):
    return (((max(time)-min(time))*x)+min(time))

C=unscaletime(f)
d=unscaletime(g)

Tf=(d-C)*24
time_increment=(time[1]-time[0])*24*3600

# From rivertestgen FEV calculation
Flowmin = (1.0-error)*flow
Flowmax = (1.0+error)*flow
Flow = []
for i in flow:
    if i>=qt:
        Flow.append((i-qt)*(time_increment))
flowmin = []
for i in Flowmin:
    if i >= qtmin:
        flowmin.append((i - qtmin) * (time_increment))
flowmax = []
for i in Flowmax:
    if i >= qtmax:
        flowmax.append((i - qtmax) * (time_increment))
FEV=sum(Flow)
FEV_max=sum(flowmax)
FEV_min=sum(flowmin)
Tfs=Tf*(60**2)
qm=(FEV/Tfs)+qt
print(qm)

scaledqm = (qm-minfl)/(maxfl-minfl)
scaledhm = (hm-minhe)/(maxhe-minhe)

ax.plot([-scaledht,-scaledht],[-1,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,-scaledhm],[-1,scaledqm],'black',linestyle='--',linewidth=1)
ax.plot([-scaledht,1],[scaledqt,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,1],[scaledqm,scaledqm],'black',linestyle='--',linewidth=1)

ax.plot([f,f,f],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([g,g,g],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([f,f],[scaledqm,scaledqt], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqm,scaledqm], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqt,scaledqt], 'black',linewidth=1.5)
ax.plot([g,g],[scaledqm,scaledqt], 'black',linewidth=1.5)
plt.annotate('', xy=(f-1/100,-1/5), xytext=(g+1/100,-1/5), arrowprops=dict(arrowstyle='<->'))

h=[]
for i in np.arange(1,number_of_days+1):
    h.append(i/number_of_days)


l=np.arange(0,max(flow)+50,50)
m=bisect.bisect(l,min(flow))

n=[]
for i in np.arange(l[m],max(flow)+50,50):
    n.append(int(i))


o=np.arange(0,max(height)+1,1)
p=bisect.bisect(o,min(height))

q=[]
for i in np.arange(o[p],max(height)+1,1):
    q.append(i)

k=[]
for i in q:
    k.append(-(i-minhe)/(maxhe-minhe))
    # OB old: k.append(-(i-min(height))/(max(height)-min(height))) 

j=[]
for i in n:
    j.append((i-minfl)/(maxfl-minfl))
    # OB old: j.append((i-min(flow))/(max(flow)-min(flow)))

ticks_x=k+h

r=[]
for i in h:
    r.append(-i)

ticks_y=r+j


s=[]
for i in np.arange(1,number_of_days+1):
    s.append(i)

s=[x+startdate for x in s]
Ticks_x=q+s
print(Ticks_x)
Ticks_y=s+n
    
tesize = 11
tsize = 13
tisize = 8

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xticks(ticks_x)
ax.set_yticks(ticks_y)
ax.set_xticklabels(Ticks_x)
ax.set_yticklabels([])
ax.set_yticklabels(Ticks_y)
lists1 = sorted(zip(*[negheight, scaledFlow_down]))
negheight1, scaledFlow_down1 = list(zip(*lists1))
lists2 = sorted(zip(*[negheight, scaledFlow_up]))
negheight1, scaledFlow_up1 = list(zip(*lists2))
ax.fill_between(negheight1,scaledFlow_down1,scaledFlow_up1,color="grey", alpha = 0.3)
ax.fill_between(scaledtime,scaledFlow_up,scaledFlow_down,color="grey", alpha = 0.3)
QtU = scaledqt*(1+error)
QtD = scaledqt*(1-error)
ax.fill_between([scaledtime[idx[0]], scaledtime[idx[-1]]], QtU, QtD, color = "grey", alpha = 0.3)
ax.tick_params(axis='x',colors='black',direction='out',length=9,width=1,labelsize=tisize)
ax.tick_params(axis='y',colors='black',direction='out',length=10,width=1, labelsize=tisize)


plt.text(-scaledht+1/100, -1,'$h_T$', size=tsize)
# General:
plt.text(-scaledhm+1/100, -1,'$h_m$', size=tsize)
# 2020 plt.text(-scaledhm-10/100, -1,'$h_m$', size=tsize)
plt.text(1, scaledqm,'$Q_m$', size=tesize)
# General:
plt.text(1, scaledqt,'$Q_T$', size=tesize)
# 2020 plt.text(1, 0.95*scaledqt,'$Q_T$', size=tesize)
plt.text((f+g/2)-0.2,-0.28,'$T_f$',size=tesize)

plt.text(0.01, 1.05,'$Q$ [m$^3$/s]', size=tesize)
plt.text(0.92, -0.23,'$t$ [day]', size=tesize)
plt.text(0.01, -1.09,'$t$ [day]', size=tesize)
plt.text(-1.1, 0.02,r'${h}$ [m]', size=tesize)

ax.scatter(0,0,color='white')

A=round(FEV/(10**6),2)
B=round(Tf,2)
C=round(ht,2)
D=round(hm,2)
E=round(qt,2)
F=round(qm,2)
Amax=round((FEV*1.16)/(10**6),2)
Amin=round((FEV*0.84)/(10**6),2)
Emax=round(max(flow),2)
H=round(max(height),2)
start_y = -0.4
spacing = 0.08

tesiz = 10
plt.text(0.4, start_y - spacing * 0, fr'$FEV \approx {A}\,\mathrm{{Mm}}^3$', size=tesiz)
plt.text(0.4, start_y - spacing * 1, fr'$FEV_{{max}} \approx {Amax}\,\mathrm{{Mm}}^3$', size=tesiz)
plt.text(0.4, start_y - spacing * 2, fr'$FEV_{{min}} \approx {Amin}\,\mathrm{{Mm}}^3$', size=tesiz)
plt.text(0.4, start_y - spacing * 3, fr'$T_f = {B}\,\mathrm{{hrs}}$', size=tesiz)
plt.text(0.4, start_y - spacing * 4, fr'$h_T = {C}\,\mathrm{{m}}$', size=tesiz)
# General:
plt.text(0.4, start_y - spacing * 5, fr'$h_m = {D}\,\mathrm{{m}}$', size=tesiz)
plt.text(0.4, start_y - spacing * 6, fr'$h_{{max}} = {H}\,\mathrm{{m}}$', size=tesiz)
# General:
plt.text(0.4, start_y - spacing * 7, fr'$Q_T = {E}\,\mathrm{{m^3/s}}$', size=tesiz)
plt.text(0.4, start_y - spacing * 8, fr'$Q_m = {F}\,\mathrm{{m^3/s}}$', size=tesiz)
plt.text(0.4, start_y - spacing * 9, fr'$Q_{{max}} = {Emax}\,\mathrm{{m^3/s}}$', size=tesiz)


# Automatically set
save_figure=True
#figure_name= f"{selected_file}_3panelGRR.png"
figure_name= f"{selected_file}_3panelGRR.pdf"

data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)

if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()


# Here a 3D square lake of depth 2m is plotted

fig = plt.figure(figsize=plt.figaspect(1)*0.6)
ax = Axes3D(fig)
plt.rcParams['axes.edgecolor']='white'
plt.rcParams["figure.figsize"] = [10,8]

ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

sl = (FEV/2)**0.5
a = [sl, sl]
b = [sl, sl]
c = [2, 0]

d = [sl, 0]
e = [sl, sl]
f = [0, 0]

g = [sl, sl]
h = [sl, 0]
i = [0, 0]

ax.plot(a, b, c, '--', color = 'k', linewidth=2)
ax.plot(d, e, f, '--', color = 'k', linewidth=2)
ax.plot(g, h, i, '--', color = 'k', linewidth=2)


x = [sl, sl, sl, 0, 0, 0, sl, sl, 0, 0, 0, 0]
y = [sl, 0, 0, 0, 0, sl, sl, 0, 0, 0, sl, sl]
z = [2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2]

ax.plot(x, y, z, color = 'k', linewidth=3)

ax.text(5*(sl/9), -5*(sl/9), 0, 'Side-length [m]', size=9)
ax.text(-sl/4, sl/4, 0, 'Side-length [m]', size=9)
ax.text(-0.02*sl, 1.01*sl, 0.8, 'Depth [m]',size=9)


ax.text(7*(sl/10), 5*(sl/4), 1, ''+str(int(round(sl)))+'m', size=9)
ax.text(14*(sl/10), 6*(sl/10), 1, ''+str(int(round(sl)))+'m', size=9)
ax.text(17*(sl/10), 6*(sl/10), 1, 'm', size=9)
ax.set_zticks([0, 2])

ax.set_xlim(sl,0)
ax.set_ylim(0,sl)
ax.set_zlim(0,10)

# plt.show()

