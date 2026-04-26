"""
Chart 07 — Menu Section Composition (Donut Chart)
==================================================
Shows which menu sections (Chicken, Beverages, Breakfast, …)
dominate dish count across all restaurants combined.
Sections with fewer than 6 dishes are collapsed into "Other".

Dataset  : dishes_clean.csv
Output   : 07_menu_donut.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Colour palette ────────────────────────────────────────────
BG      = '#0F172A'
TEXT    = '#F1F5F9'
MUTED   = '#94A3B8'
PALETTE = [
    '#2563EB', '#16A34A', '#DC2626', '#D97706', '#7C3AED',
    '#0891B2', '#DB2777', '#65A30D', '#EA580C', '#4338CA',
]

# ── Load & prepare ────────────────────────────────────────────
dishes = pd.read_csv('dishes_clean.csv')

sec_counts = dishes['menu_section'].value_counts()

# Keep sections with ≥ 6 dishes; roll the rest into "Other"
major = sec_counts[sec_counts >= 6]
other_total = sec_counts[sec_counts < 6].sum()

if other_total > 0:
    other = pd.Series({'Other': other_total})
    sec_plot = pd.concat([major, other]).sort_values(ascending=False)
else:
    sec_plot = major.sort_values(ascending=False)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
ax.set_facecolor(BG)

wedge_colors = [PALETTE[i % len(PALETTE)] for i in range(len(sec_plot))]

wedges, texts, autotexts = ax.pie(
    sec_plot.values,
    labels=sec_plot.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=wedge_colors,
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    pctdistance=0.78,
    textprops={'color': TEXT, 'fontsize': 9}
)

# Style percentage labels
for at in autotexts:
    at.set_fontsize(8)
    at.set_color('#F8FAFC')
    at.set_fontweight('bold')

# Centre annotation
ax.text(0, 0, f'{len(dishes)}\ndishes',
        ha='center', va='center',
        color=TEXT, fontsize=13, fontweight='bold')

# ── Formatting ────────────────────────────────────────────────
ax.set_title(
    'Menu Section Composition',
    color=TEXT, fontsize=14, fontweight='bold', pad=15
)

fig.text(
    0.5, 0.02,
    'Chicken + Beverages + Breakfast account for ~42 % of all dish slots',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('07_menu_donut.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 07_menu_donut.png")
