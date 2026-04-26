"""
Chart 04 — Price Distribution per Restaurant (Violin + Strip Plot)
==================================================================
Shows the full price spread for every restaurant's menu,
with individual dish prices overlaid as white dots.

Dataset  : dishes_clean.csv
Output   : 04_price_violin.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

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
dishes = pd.read_csv('dishes_clean.csv')

# Order restaurants by descending median price (left = most expensive)
order = (
    dishes.groupby('restaurant_name')['price']
    .median()
    .sort_values(ascending=False)
    .index
)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7), facecolor=BG)
ax.set_facecolor(CARD)

# Violin layer — shows density / shape of the distribution
sns.violinplot(
    data=dishes,
    x='restaurant_name', y='price',
    order=order,
    palette=PALETTE[: len(order)],
    inner=None,          # remove built-in inner marks; we add our own
    cut=0,               # clip at data boundaries
    ax=ax
)

# Strip layer — individual dish price dots
sns.stripplot(
    data=dishes,
    x='restaurant_name', y='price',
    order=order,
    color='white',
    alpha=0.50,
    size=3.5,
    jitter=True,
    ax=ax
)

# ── Formatting ────────────────────────────────────────────────
ax.set_xticklabels(order, rotation=35, ha='right', color=TEXT, fontsize=9)
ax.set_xlabel('',                    color=MUTED, fontsize=10)
ax.set_ylabel('Price (EGP)',         color=MUTED, fontsize=10)
ax.set_title(
    'Price Distribution per Restaurant\n(violin = density · white dots = individual dishes)',
    color=TEXT, fontsize=13, fontweight='bold', pad=14
)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(axis='y', color='#334155', linewidth=0.5, alpha=0.6)

plt.tight_layout()
plt.savefig('04_price_violin.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 04_price_violin.png")
