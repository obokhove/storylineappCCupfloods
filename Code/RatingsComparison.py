# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 22:52:29 2026

@author: Natasha Pickard
"""
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# FILE PATHS (yours)
# =========================
hydro_file = r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Aire Armley 2020 Stage and Flow.csv"
ratings_file = r"C:\Users\Natasha Pickard\OneDrive - University of Leeds\Year 3\MATH3001\FINAL\Armley Ratings Data 2016.csv"

# =========================
# LOAD DATA
# =========================
hydro = pd.read_csv(hydro_file)
ratings = pd.read_csv(ratings_file)

hydro.columns = hydro.columns.astype(str).str.strip()
ratings.columns = ratings.columns.astype(str).str.strip()

t = hydro["Time"].to_numpy()
h = hydro["Height"].to_numpy()
Q_ea = hydro["Flow"].to_numpy()

upper_col = "Upper limit"
c_col = "Aire_C"
a_col = "Aire_a"
b_col = "Aire_b"

ratings = ratings.sort_values(upper_col).reset_index(drop=True)

hk = ratings[upper_col].to_numpy(dtype=float)
ck = ratings[c_col].to_numpy(dtype=float)
ak = ratings[a_col].to_numpy(dtype=float)
bk = ratings[b_col].to_numpy(dtype=float)

hk_low = np.concatenate(([0.0], hk[:-1]))

def Q_from_rating_curve(h_vals: np.ndarray) -> np.ndarray:
    Q = np.zeros_like(h_vals, dtype=float)

    for i, hi in enumerate(h_vals):
        idx = np.where((hk_low <= hi) & (hi < hk))[0]
        if len(idx) == 0:
            k = 0 if hi < hk_low[0] else len(hk) - 1
        else:
            k = int(idx[0])

        base = hi - ak[k]
        if base < 0:
            base = 0.0
        Q[i] = ck[k] * (base ** bk[k])

    return Q

Q_calc = Q_from_rating_curve(h)

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(t, Q_ea,
        color="blue",
        linewidth=2,
        label="EA Flow")

ax.plot(t, Q_calc,
        color="orange",
        linestyle="--",
        linewidth=2,
        label="Calculated Flow (from rating coefficients & height)")

ax.set_xlabel("Time (days)", fontsize = 15)
ax.set_ylabel("Discharge (m³/s)", fontsize = 15)

ax.set_ylim(0, 250)
ax.grid(True, linewidth=1, alpha=0.6)
ax.tick_params(axis="both", labelsize=12)

# ---------- Box around plot ----------
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.2)
    spine.set_color("black")

# ---------- Legend formatting ----------
leg = ax.legend(loc="upper right", frameon=True, fontsize = 15)
leg.get_frame().set_facecolor("white")
leg.get_frame().set_edgecolor("black")
leg.get_frame().set_linewidth(1)

plt.tight_layout()
plt.show()