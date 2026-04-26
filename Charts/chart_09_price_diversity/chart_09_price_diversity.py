"""
Chart 09 — Price Diversity: Avg Price vs Price Std Dev
=======================================================
Plots each restaurant on two axes:
  X  =  average menu price      (how expensive overall)
  Y  =  price standard deviation (how diverse the menu is)
Bubble size encodes review volume (reach / popularity).

Dataset  : restaurants_clean.csv, categories_clean.csv, regions_clean.csv
Output   : 09_price_diversity.png
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
fig, ax = plt.subplots(figsize=(11, 7), facecolor=BG)
ax.set_facecolor(CARD)

for i, (_, row) in enumerate(merged.iterrows()):
    bubble_size = row['num_reviews'] / 3_000     # scale down for readability
    ax.scatter(
        row['avg_price'],
        row['price_std_dev'],
        s=bubble_size,
        color=PALETTE[i % len(PALETTE)],
        alpha=0.85,
        edgecolors='white', linewidth=0.5,
        zorder=5
    )
    ax.annotate(
        row['restaurant_name'],
        (row['avg_price'], row['price_std_dev']),
        textcoords='offset points', xytext=(7, 5),
        fontsize=8.5, color=TEXT, fontweight='bold'
    )

# ── Reference lines (median of each axis) ─────────────────────
med_price = merged['avg_price'].median()
med_std   = merged['price_std_dev'].median()

ax.axvline(med_price, color='#334155', linestyle='--', linewidth=1, alpha=0.7,
           label=f'Median avg price  EGP {med_price:.0f}')
ax.axhline(med_std,   color='#334155', linestyle=':',  linewidth=1, alpha=0.7,
           label=f'Median std dev  EGP {med_std:.0f}')

ax.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8.5)

# ── Formatting ────────────────────────────────────────────────
ax.set_xlabel('Average Price (EGP)',       color=MUTED, fontsize=10)
ax.set_ylabel('Price Std Deviation (EGP)', color=MUTED, fontsize=10)
ax.set_title(
    'Price Diversity: Avg Price vs Price Std Dev\n(bubble size = review volume)',
    color=TEXT, fontsize=13, fontweight='bold', pad=14
)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(True, color='#334155', linewidth=0.4, alpha=0.5)

fig.text(
    0.5, 0.01,
    'Upper-right = expensive & diverse menu  |  Lower-left = cheap & focused menu',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('09_price_diversity.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 09_price_diversity.png")
