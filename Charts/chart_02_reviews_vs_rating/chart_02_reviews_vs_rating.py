"""
Chart 02 — Reviews vs Rating  (Bubble Chart)
=============================================
Bubble size  = number of menu items (num_dishes)
Dataset      : restaurants_clean.csv, categories_clean.csv, regions_clean.csv
Output       : 02_reviews_vs_rating.png
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

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7), facecolor=BG)
ax.set_facecolor(CARD)

for i, (_, row) in enumerate(merged.iterrows()):
    bubble_size = row['num_dishes'] * 8          # scale bubble by menu size
    ax.scatter(
        row['rating'],
        row['num_reviews'] / 1_000,              # convert to thousands
        s=bubble_size,
        color=PALETTE[i % len(PALETTE)],
        alpha=0.85,
        edgecolors='white', linewidth=0.6,
        zorder=5
    )
    ax.annotate(
        row['restaurant_name'],
        (row['rating'], row['num_reviews'] / 1_000),
        textcoords='offset points', xytext=(9, 5),
        fontsize=8.5, color=TEXT, fontweight='bold'
    )

# ── Formatting ────────────────────────────────────────────────
ax.set_xlabel('Rating',             color=MUTED, fontsize=10)
ax.set_ylabel('Reviews (thousands)', color=MUTED, fontsize=10)
ax.set_title(
    'Reviews vs Rating\n(bubble size = number of menu items)',
    color=TEXT, fontsize=13, fontweight='bold', pad=12
)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(True, color='#334155', linewidth=0.4, alpha=0.5)

fig.text(
    0.5, 0.01,
    "McDonald's dominates in reach · Buffalo Burger leads in rating",
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('02_reviews_vs_rating.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 02_reviews_vs_rating.png")
