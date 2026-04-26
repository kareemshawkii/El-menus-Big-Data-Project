"""
Chart 03 — Average Menu Price by Restaurant (Vertical Bar Chart)
================================================================
Dataset  : restaurants_clean.csv, categories_clean.csv, regions_clean.csv
Output   : 03_avg_price.png
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

# ── Load & merge ──────────────────────────────────────────────
restaurants = pd.read_csv('restaurants_clean.csv')
categories  = pd.read_csv('categories_clean.csv')
regions     = pd.read_csv('regions_clean.csv')

merged = restaurants.merge(
    categories[['category_id', 'category_name']], on='category_id', how='left'
).merge(
    regions[['zone_id', 'zone_name', 'area_name']].drop_duplicates('zone_id'),
    on='zone_id', how='left'
)

# Sort descending so the most expensive bar is on the left
df = merged.sort_values('avg_price', ascending=False)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6), facecolor=BG)
ax.set_facecolor(CARD)

bars = ax.bar(
    df['restaurant_name'],
    df['avg_price'],
    color=[PALETTE[i % len(PALETTE)] for i in range(len(df))],
    edgecolor='none',
    width=0.6
)

# Value labels above each bar
for bar, val in zip(bars, df['avg_price']):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 3,
        f'EGP {val:.0f}',
        ha='center', va='bottom',
        color=TEXT, fontsize=9, fontweight='bold'
    )

# ── Formatting ────────────────────────────────────────────────
ax.set_xticklabels(
    df['restaurant_name'], rotation=30, ha='right',
    color=TEXT, fontsize=9
)
ax.set_ylabel('Average Price (EGP)', color=MUTED, fontsize=10)
ax.set_title(
    'Average Menu Price by Restaurant',
    color=TEXT, fontsize=14, fontweight='bold', pad=14
)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(axis='y', color='#334155', linewidth=0.5, alpha=0.6)

plt.tight_layout()
plt.savefig('03_avg_price.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 03_avg_price.png")
