"""
Chart 05 — Top 15 Food Categories by Restaurant Count (Horizontal Bar)
=======================================================================
Reveals which food categories are the most saturated markets
and which remain underserved.

Dataset  : categories_clean.csv
Output   : 05_category_market.png
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

# ── Load data ─────────────────────────────────────────────────
categories = pd.read_csv('categories_clean.csv')

# Keep top 15 by restaurant count, sorted ascending so the
# longest bar (most restaurants) is at the top of the chart
top15 = (
    categories
    .sort_values('restaurants_count', ascending=True)
    .tail(15)
)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8), facecolor=BG)
ax.set_facecolor(CARD)

bars = ax.barh(
    top15['category_name'],
    top15['restaurants_count'],
    color=[PALETTE[i % len(PALETTE)] for i in range(len(top15))],
    edgecolor='none',
    height=0.65
)

# Value label at the end of each bar
for bar, val in zip(bars, top15['restaurants_count']):
    ax.text(
        val + 1.5,
        bar.get_y() + bar.get_height() / 2,
        str(val),
        va='center', ha='left',
        color=TEXT, fontsize=9, fontweight='bold'
    )

# ── Formatting ────────────────────────────────────────────────
ax.set_xlabel('Number of Restaurants', color=MUTED, fontsize=10)
ax.set_title(
    'Top 15 Food Categories by Restaurant Count',
    color=TEXT, fontsize=14, fontweight='bold', pad=14
)
ax.tick_params(axis='y', colors=TEXT,  labelsize=10)
ax.tick_params(axis='x', colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(axis='x', color='#334155', linewidth=0.5, alpha=0.6)

fig.text(
    0.5, 0.01,
    'Desserts, Salads & Sandwiches are the most saturated markets',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('05_category_market.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 05_category_market.png")
