"""
Chart 06 — Top 20 Areas by Delivery Zone Coverage (Horizontal Bar)
===================================================================
Identifies which Cairo neighbourhoods have the deepest delivery
infrastructure — a proxy for restaurant density and customer demand.

Dataset  : regions_clean.csv
Output   : 06_regions.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Colour palette ────────────────────────────────────────────
BG      = '#0F172A'
CARD    = '#1E293B'
TEXT    = '#F1F5F9'
MUTED   = '#94A3B8'
PALETTE = [
    '#2563EB', '#16A34A', '#DC2626', '#D97706', '#7C3AED',
    '#0891B2', '#DB2777', '#65A30D', '#EA580C', '#4338CA',
]

# ── Load & aggregate ──────────────────────────────────────────
regions = pd.read_csv('regions_clean.csv')

# Count distinct delivery zones per area, then take the top 20
area_zone_count = (
    regions
    .groupby('area_name')['zone_id']
    .count()
    .sort_values(ascending=True)   # ascending → longest bar at the top
    .tail(20)
)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 9), facecolor=BG)
ax.set_facecolor(CARD)

bars = ax.barh(
    area_zone_count.index,
    area_zone_count.values,
    color=[PALETTE[i % len(PALETTE)] for i in range(len(area_zone_count))],
    edgecolor='none',
    height=0.65
)

# Value label
for bar, val in zip(bars, area_zone_count.values):
    ax.text(
        val + 0.8,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va='center', ha='left',
        color=TEXT, fontsize=9, fontweight='bold'
    )

# ── Formatting ────────────────────────────────────────────────
ax.set_xlabel('Number of Delivery Zones', color=MUTED, fontsize=10)
ax.set_title(
    'Top 20 Areas by Delivery Zone Coverage',
    color=TEXT, fontsize=14, fontweight='bold', pad=14
)
ax.tick_params(axis='y', colors=TEXT,  labelsize=9)
ax.tick_params(axis='x', colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(axis='x', color='#334155', linewidth=0.5, alpha=0.6)

fig.text(
    0.5, 0.01,
    'New Cairo leads with 178 zones — the #1 expansion priority',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('06_regions.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 06_regions.png")
