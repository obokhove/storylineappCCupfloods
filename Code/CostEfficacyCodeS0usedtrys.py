# -*- coding: utf-8 -*-
""" Created on Thu Apr 10 19:36:35 2025; update by Onno Bokhove 14-03-2026 vv
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
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2015 Armley 2030 Upper": {
        "FEV": 20.31,  # Mm³
        "mitigations": {
            "Walls": (13.24, 75.6),
            "Calverley": (1.8, 10),
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2020 Armley 2050 Upper": {
        "FEV": 5.16,  # Mm³
        "mitigations": {
            "Walls": (5.15353, 75.6),
            "Calverley": (1.8, 10),
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2015 Armley 2050 Upper": {
        "FEV": 24.49,  # Mm³
        "mitigations": {
            "Walls": (14.96, 75.6),
            "Calverley": (1.8, 10),
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2020 Armley 2080 Upper": {
        "FEV": 13.57,  # Mm³
        "mitigations": {
            "Walls": (12.617, 75.6),
            "Calverley": (1.8, 10),
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2015 Armley 2080 Upper": {
        "FEV": 38.33,  # Mm³
        "mitigations": {
            "Walls": (20, 75.6),
            "Calverley": (1.8, 10),
            "Rodley": (2.2, 14),
            "GRR": (0.65, 10),
            "NFM": (0.47, 4),
            "Beavers": (0.0935, 1),
            "Cononley+Holden": (4.1, 35)
        }
    },
    "2015 Armley 2015": {
        "FEV": 9.36,  # Mm³
        "mitigations": {
            "Walls": (7.97, 89),
            "GRR": (0.66, 10),
            "Calverley": (0.7, 10),
            #""Rodley": (1, 14),
            #"NFM": (0.47, 4),
            #"Beavers": (0.0935, 1),
            #"Cononley+Holden": (4.2, 35)
        }
    }
}

floods = {
    "2015 Armley 2080 Upper": {
        "FEV": 9.33,  # Mm³
        "mitigations": {
            "Walls": (0.855*9.33, 89),
            "GRR": (0.07*9.33, 10), #  0.66
            "Calverley": (0.075*9.33, 10), # 0.7
            #""Rodley": (1, 14),
            #"NFM": (0.47, 4),
            #"Cononley+Holden": (4.2, 35)
        }
    }
}

extra = {
    "2015 Armley 2080 Upper": {
        "mitigations": {
            "Calverley+": (0.06*9.33, 0), # 1.26-0.7=0.56
            "Beavers": (0.037*9.33, 1), # 0.35
        }
    }
}

# Enhanced version: proper axis ticks, labels, proportional layout, and title placement
def plot_square_lake_enhanced(name, fev, mitigations, extra=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    size = math.sqrt(fev*10**6/ 2)

    total_vol = sum(vol for vol, _ in mitigations.values())
    total_cost = sum(cost for _, cost in mitigations.values())
    total_percent = total_vol / fev * 100
    colors = plt.cm.Paired(np.linspace(0, 1, len(mitigations)))

    # Fill entire square if overcapacity
    if total_vol >= fev: # OB
        ax.add_patch(patches.Rectangle((0, 0), size, size, color='lightblue', alpha=0.6)) # OB

    x = 0
    label_base_y = size
    label_spacing = size / (len(mitigations) + 1)

    for i, (name_m, (vol, cost)) in enumerate(mitigations.items()):
        width = vol / fev * size
        percent = vol / fev * 100
        cost_eff = cost / percent if percent != 0 else 0
        label = f"{name_m}\n{percent:.1f}%\n\u00A3{cost:.1f}M\n\u00A3{cost_eff:.1f}M/%"

        # if total_vol < fev: # OB
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
        # OLD: if x >= size: # OB
        # OLD:    break  # OB
        xtot = x

    if extra and name in extra:
        extra_mits = extra[name]["mitigations"]
        x_top = x  # separate cursor for stacking along the TOP
        ytopr = 0
        colors_extra = plt.cm.autumn(np.linspace(0.4, 0.9, len(extra_mits)))
        for i, (ename, (vol, cost)) in enumerate(extra_mits.items()):
            w_top = vol / fev * size  # width at top
            poly = patches.Polygon([
                (x, 0),                      # bottom point (shared)
                (x, 0),
                (x_top + w_top, size),       # top right
                (x_top, size)                # top left
            ],
            closed=True,
            facecolor=colors_extra[i],
            edgecolor='black',
            linestyle='-',
            linewidth=1.0,
            alpha=0.5,
            zorder=20)
            ax.add_patch(poly)
            # Label
            percent_top = vol / fev * 100
            label = f"{ename}\n0%→{percent_top:.1f}%\n£{cost}M"
            # ax.text(x_top + w_top / 2, size + 0.05 * size,label, ha='center', va='bottom',fontsize=8, color=colors_extra[i])
            ax.text(x_top+w_top/2, size-0.35*size+ytopr,label, ha='center', va='bottom',fontsize=10, color='black')
            x_top += w_top  # move along TOP only
            ytopr = -0.15*size

        # update total width for axis scaling
        x = x_top

        
        
    #  OLD: ax.set_xlim(0, size + 2)
    ax.set_xlim(0, max(size, x) + 2)
    ax.set_ylim(0, size + 1)
    tick_interval = size / 5
    ax.set_xticks(np.arange(0, size + 0.1, tick_interval))
    ax.set_yticks(np.arange(0, size + 0.1, tick_interval))
    ax.set_xlabel("Sidelength (m)", fontsize=10)
    ax.set_ylabel("Sidelength (m)", fontsize=10)

    # Title positioned just above the centre of the square
    ax.text(size / 2, size + 0.3, f"$S_0$: FEV ≈ {size:.0f}$^2$ m$^2$ × 2m ≈ {fev:.2f}Mm$^3$",
            ha='center', va='bottom', fontsize=12)
    total_arrow_y = size + 0.05
    # OLD: ax.annotate('', xy=(x, 100), xytext=(0, 100),arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    top_yy = size-0.1*size
    ax.annotate('', xy=(xtot, top_yy), xytext=(0, top_yy), arrowprops=dict(arrowstyle='<->', color='black', linewidth=1.5))
    # OLD: ax.text(size / 2, 200,
    top_y = size - 0.1 * size   # dynamic spacing
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
    #plt.show()


# Render for all flood scenarios
for name, data in floods.items():
    #
    plot_square_lake_enhanced(name, data["FEV"], data["mitigations"], extra)
    # No extras: plot_square_lake_enhanced(name, data["FEV"], data["mitigations"], extra=None)
    

# Automatically set
save_figure=True
# figure_name= f"costeffisqlS0plus.png"
figure_name= f"costeffisqlS0plus.pdf"

data_path = 'data/'
if save_figure:
    save_path=os.path.join(data_path, figure_name)
        
if save_figure:
    plt.savefig(save_path,dpi=300)
else:
    plt.show()

