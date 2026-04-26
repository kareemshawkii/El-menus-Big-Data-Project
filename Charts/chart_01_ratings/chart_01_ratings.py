"""
Chart 01 — Restaurant Ratings Comparison (Horizontal Bar Chart)
================================================================
Dataset required : restaurants_clean.csv, categories_clean.csv, regions_clean.csv
Output           : 01_ratings.png
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Colour palette ────────────────────────────────────────────
BG    = '#0F172A'
CARD  = '#1E293B'
TEXT  = '#F1F5F9'
MUTED = '#94A3B8'
ACCENT = '#38BDF8'
GREEN  = '#22C55E'
YELLOW = '#FACC15'
RED    = '#EF4444'

# ── Load & merge data ─────────────────────────────────────────
restaurants = pd.read_csv('restaurants_clean.csv')
categories  = pd.read_csv('categories_clean.csv')
regions     = pd.read_csv('regions_clean.csv')

merged = restaurants.merge(
    categories[['category_id', 'category_name']], on='category_id', how='left'
).merge(
    regions[['zone_id', 'zone_name', 'area_name']].drop_duplicates('zone_id'),
    on='zone_id', how='left'
)

# ── Sort ascending so best bar appears at the top ────────────
df = merged.sort_values('rating', ascending=True)

# ── Colour-code by rating tier ────────────────────────────────
bar_colors = [
    GREEN  if r >= 4.5 else
    YELLOW if r >= 4.3 else
    RED
    for r in df['rating']
]

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6), facecolor=BG)
ax.set_facecolor(CARD)

bars = ax.barh(
    df['restaurant_name'], df['rating'],
    color=bar_colors, edgecolor='none', height=0.6
)

# Value labels on each bar
for bar, val in zip(bars, df['rating']):
    ax.text(
        val + 0.003,
        bar.get_y() + bar.get_height() / 2,
        f'{val:.4f}',
        va='center', ha='left',
        color=TEXT, fontsize=10, fontweight='bold'
    )

# Reference line
ax.axvline(4.5, color=ACCENT, linestyle='--', linewidth=1.2,
           alpha=0.7, label='4.5 Elite threshold')

# ── Formatting ────────────────────────────────────────────────
ax.set_xlim(4.0, 4.85)
ax.set_xlabel('Rating', color=MUTED, fontsize=10)
ax.set_title('Restaurant Ratings Comparison',
             color=TEXT, fontsize=14, fontweight='bold', pad=14)
ax.tick_params(colors=MUTED, labelsize=9)
ax.tick_params(axis='y', colors=TEXT, labelsize=10)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(axis='x', color='#334155', linewidth=0.5, alpha=0.6)
ax.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=9)

fig.text(
    0.5, 0.01,
    'Green = Elite (≥ 4.5)  |  Yellow = Good (≥ 4.3)  |  Red = Needs Improvement',
    ha='center', color=MUTED, fontsize=8.5
)

plt.tight_layout()
plt.savefig('01_ratings.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("Saved → 01_ratings.png")
