# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 19:36:35 2025; update by Onno Bokhove 14-03-2026 vv
@author: Natasha Pickard
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import os.path

# Define FEV values and mitigation contributions for both floods
#mitigation:FEV,total cost
floodsold = {
    "2020 Armley 2030 Upper": {
        "FEV": 3.1,  # Mm³
        "mitigations": {
            "Walls": (8.03, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    },
    "2015 Armley 2030 Upper": {
        "FEV": 20.31,  # Mm³
        "mitigations": {
            "Walls": (13.24, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    },
    "2020 Armley 2050 Upper": {
        "FEV": 5.16,  # Mm³
        "mitigations": {
            "Walls": (5.15353, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    },
    "2015 Armley 2050 Upper": {
        "FEV": 24.49,  # Mm³
        "mitigations": {
            "Walls": (14.96, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    },
    "2020 Armley 2080 Upper": {
        "FEV": 13.57,  # Mm³
        "mitigations": {
            "Walls": (12.617, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    },
    "2015 Armley 2080 Upper": {
        "FEV": 38.33,  # Mm³
        "mitigations": {
            "Walls": (20, 75.6),
            "Calverley": (1.8, 10),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4)
        }
    }
}

floods = {
        "2015 Armley 2080 Upper": {
        "FEV": 30.46,  # Mm³
        "mitigations": {
            "Walls": (15.65, 79), # % 51.4% 15.65Mm^3
            "GRR": (1.04, 10),  # 0.66Mm^3 3.4%
            "Calverley": (0.7, 10), # 2.3%
            "Rodley": (1, 14), # 3.3%
            "Cononley+Holden": (4.2, 35), # 13.8%
            # 1/9
            "AFM+NFM": (0.46, 16.84), # 1.5% or 0.46Mm^3
            # 1/3 "AFM+NFM": (1.39, 16.84), # 3*1.5% or 3*0.46Mm^3 
            #"NFM": (0.0, 2.84),
            #"AFM": (0.0, 2.85),
            #"Beavers": (0.0, 0.5),
        }
    }
}

# Set above to 1/3: frac = 1/3
# Set above to 1/9: 
frac = 1/9 
omfrac = 1-frac # one minus frac
extra = {
    "2015 Armley 2080 Upper": {
        "mitigations": {
            "NFM+AFM0": (0*30.46, 0), # 0 for 8/9 or 2/3 of vertical or height of lake as a line drawing so a block of 0*9.33 width and upsize 1/9 starting in last drwaing of floods
            "NFM+AFM9": (0.136*30.46, 0), # 4.13 for 1/9 or 1/3 of vertical  or height as a line drawing so as a block of 0.136*30.46 starting in last drawing of floods
            "Beavers": (0.015*30.46, 1), # 0.46, added as triangle. 
        }
    }
}

# Enhanced version: proper axis ticks, labels, proportional layout, and title placement
positions = {}
def plot_square_lake_enhanced(name, fev, mitigations,extra=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    size = math.sqrt(fev*10**6/ 2)

    total_vol = sum(vol for vol, _ in mitigations.values())
    total_cost = sum(cost for _, cost in mitigations.values())
    total_percent = total_vol / fev * 100
    colors = plt.cm.Paired(np.linspace(0, 1, len(mitigations)))

    # Fill entire square if overcapacity
    if total_vol >= fev:
        ax.add_patch(patches.Rectangle((0, 0), size, size, color='lightblue', alpha=0.6))

    x = 0
    label_base_y = size
    label_spacing = size / (len(mitigations) + 1)

    for i, (name_m, (vol, cost)) in enumerate(mitigations.items()):
        width = vol / fev * size
        positions[name_m] = (x, width)   # 👈 store start + width
        percent = vol / fev * 100
        cost_eff = cost / percent if percent != 0 else float('inf') #  was 0
        label = f"{name_m}\n{percent:.1f}%\n\u00A3{cost:.1f}M, \u00A3{cost_eff:.1f}M/%"

        if total_vol < fev:
            rect = patches.Rectangle((x, 0), width, size, color=colors[i], alpha=0.8)
            ax.add_patch(rect)

        label_y = label_base_y - (i + 1) * label_spacing
        # OLD: label_x = size + 0.4
        label_x = max(size, x) + 0.4
        # OLD: arrow_start_x = 0 if total_vol >= fev else x
        # OLD: arrow_end_x = size if total_vol >= fev else x + width
        arrow_start_x = x
        arrow_end_x = x + width
        arrow_y = label_y - 0.2

        ax.annotate('', xy=(arrow_end_x, arrow_y), xytext=(arrow_start_x, arrow_y),
                    arrowprops=dict(arrowstyle='<->', color='black'))

        ax.annotate(label,
                    xy=(label_x-(0.05*size), label_y+(0.06*size)),
                    xytext=((arrow_start_x + arrow_end_x) / 2-(0.05*size), label_y+(0.06*size)),
                    ha='left', va='center', fontsize=9)
        x += width
        # OLD: if x >= size:
        # OLD:   break
        xtot = x
        
    if extra and name in extra:
        extra_mits = extra[name]["mitigations"]
        # 🔴 rewind to AFM+NFM position
        if "AFM+NFM" in positions:
            x_extra, w_afm = positions["AFM+NFM"]
        else:
            x_extra = x  # fallback
        for ename, (vol, cost) in extra_mits.items():
            # --- CASE 1: split blocks (NFM+AFM) ---
            if "NFM+AFM" in ename:
                w = vol / fev * size
                # height logic: 1/9 vs 8/9
                if "0" in ename:
                    y0 = size*frac # OB was 2/9
                    h = size*omfrac # size*(8/9)
                else:  # "9"
                    y0 = size*omfrac
                    h = size*frac # size*(1/9) 
                rect = patches.Rectangle((x_extra, y0),w,h,facecolor='orange',alpha=0.3,
                    edgecolor='purple',linewidth=1.2,zorder=15)
                ax.add_patch(rect)

                # label (center of block)
                percent = vol / fev * 100
                ax.text(x_extra + w/2, y0+h/3,  # adjust h/2 or h/3 by hand
                        f"{ename}\n{percent:.1f}%",ha='center', va='center',fontsize=8, color='purple')
                
                x_extra += w

            # --- CASE 2: triangle (Beavers) ---
            elif "Beavers" in ename:
                w_top = vol / fev * size
                x_extraa = x_extra  # OB was x_extraa = x_extra
                poly = patches.Polygon([(x_extraa, 0),(x_extraa, 0),(x_extraa + w_top, size),(x_extraa, size)],
                closed=True,facecolor='silver',edgecolor='black',linestyle='-',
                linewidth=1.5,alpha=0.6,zorder=20)

                ax.add_patch(poly)
                percent = vol / fev * 100
                ax.text(x_extraa+w_top/2, size-0.5*size,
                    f"{ename}\n0%→{percent:.1f}%",ha='center', va='bottom',fontsize=8, color='black')
                x_extra += w_top

        # update total width
        x = x_extra
        # xtot = x


    # OLD: ax.set_xlim(0, size + 2)
    ax.set_xlim(0, max(size, x) + 2)
    ax.set_ylim(0, size + 1)
    tick_interval = size / 5
    ax.set_xticks(np.arange(0, size + 0.1, tick_interval))
    ax.set_yticks(np.arange(0, size + 0.1, tick_interval))
    ax.set_xlabel("Sidelength (m)", fontsize=10)
    ax.set_ylabel("Sidelength (m)", fontsize=10)

    # Title positioned just above the centre of the square
    ax.text(size / 2, size + 0.3, f"$S_1$: FEV ≈ {size:.0f}$^2$ m$^2$ × 2m ≈ {fev:.2f}Mm$^3$",
            ha='center', va='bottom', fontsize=12)
    total_arrow_y = size + 0.05
    # OLD: ax.annotate('', xy=(x, 100), xytext=(0, 100),arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    top_yy = size-0.95*size
    ax.annotate('', xy=(xtot, top_yy), xytext=(0, top_yy), arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    # OLD: ax.text(size / 2, 200,
    top_y = size - 0.9 * size   # dynamic spacing
    ax.text(xtot / 2, top_y, f"Total: {total_percent:.1f}% FEV mitigated, \u00A3{total_cost:.1f}M",
            ha='center', va='bottom', fontsize=10, weight='bold')

    ax.set_aspect('equal')
    ax.tick_params(axis='both', labelsize=9)
    # Bold square edges with high zorder to bring to front
    ax.plot([0, size], [0, 0], 'k-', linewidth=2, zorder=10)          # Bottom
    ax.plot([0, size], [size, size], 'k-', linewidth=2, zorder=10)    # Top
    ax.plot([0, 0], [0, size], 'k-', linewidth=2, zorder=10)          # Left
    ax.plot([size, size], [0, size], 'k-', linewidth=2, zorder=10)    # Right
    plt.tight_layout()
    # plt.show()

# Render for all flood scenarios
for name, data in floods.items():
    # plot_square_lake_enhanced(name, data["FEV"], data["mitigations"],extra=None)
    #
    plot_square_lake_enhanced(name, data["FEV"], data["mitigations"],extra)

# Automatically set
save_figure=True
# figure_name= f"costeffisqlS1plus.png"
figure_name= f"costeffisqlS1plus.pdf"
data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)
    
if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()
