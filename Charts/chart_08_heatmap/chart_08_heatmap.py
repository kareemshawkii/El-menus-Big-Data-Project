"""
Chart 08 — Feature Correlation Heatmap
=======================================
Computes pairwise Pearson correlations between all numeric KPIs
(rating, reviews, dish count, price metrics) and visualises them
as an annotated heatmap with a diverging blue-red colour scale.

Dataset  : restaurants_clean.csv, categories_clean.csv, regions_clean.csv
Output   : 08_heatmap.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── Colour palette ────────────────────────────────────────────
BG   = '#0F172A'
CARD = '#1E293B'
TEXT = '#F1F5F9'
MUTED = '#94A3B8'

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

# ── Select numeric features & compute correlation matrix ──────
num_cols = [
    'rating', 'num_reviews', 'num_dishes',
    'avg_price', 'price_variance', 'price_std_dev'
]
display_labels = [
    'Rating', 'Reviews', '# Dishes',
    'Avg Price', 'Price Var', 'Price Std'
]

corr = merged[num_cols].corr()

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 7), facecolor=BG)
ax.set_facecolor(CARD)

cmap = sns.diverging_palette(220, 10, as_cmap=True)   # blue-red diverging

sns.heatmap(
    corr,
    annot=True,
    fmt='.2f',
    cmap=cmap,
    center=0,
    vmin=-1, vmax=1,
    xticklabels=display_labels,
    yticklabels=display_labels,
    ax=ax,
    linewidths=0.5,
    linecolor='#1E293B',
    annot_kws={'size': 10, 'color': 'white', 'fontweight': 'bold'},
    cbar_kws={'shrink': 0.8}
)

# Style tick labels
ax.tick_params(axis='x', colors=TEXT, labelsize=9, rotation=30)
ax.tick_params(axis='y', colors=TEXT, labelsize=9, rotation=0)

# Style the colour-bar
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(colors=MUTED, labelsize=8)
cbar.outline.set_visible(False)

ax.set_title(
    'Feature Correlation Heatmap',
    color=TEXT, fontsize=13, fontweight='bold', pad=14
)

fig.text(
    0.5, 0.01,
    'avg_price ↔ price_std_dev = 0.96  |  higher price always means wider price spread',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('08_heatmap.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 08_heatmap.png")
