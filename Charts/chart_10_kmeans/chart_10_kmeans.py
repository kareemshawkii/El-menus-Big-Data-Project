"""
Chart 10 — K-Means Clustering: Rating × Median Price  (k = 3)
==============================================================
Segments restaurants into 3 strategic clusters using:
  X  =  customer rating
  Y  =  median dish price  (derived from dishes_clean.csv)

Steps
-----
1. Compute median price per restaurant from the dishes dataset.
2. Merge with restaurant KPIs.
3. StandardScaler → KMeans(k=3).
4. Plot clusters with colour-coded markers and soft ellipse halos.

Dataset  : restaurants_clean.csv, categories_clean.csv,
           regions_clean.csv,     dishes_clean.csv
Output   : 10_kmeans.png
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ── Colour palette ────────────────────────────────────────────
BG      = '#0F172A'
CARD    = '#1E293B'
TEXT    = '#F1F5F9'
MUTED   = '#94A3B8'
GREEN   = '#22C55E'
YELLOW  = '#FACC15'
ACCENT  = '#38BDF8'
PALETTE = [
    '#2563EB', '#16A34A', '#DC2626', '#D97706', '#7C3AED',
    '#0891B2', '#DB2777', '#65A30D', '#EA580C', '#4338CA',
]

CLUSTER_LABELS = {
    0: 'Budget-Friendly Champions',
    1: 'Mid-Market Stars',
    2: 'Value Leaders',
}
CLUSTER_COLORS = {0: GREEN, 1: YELLOW, 2: ACCENT}

# ── Load & merge ──────────────────────────────────────────────
restaurants = pd.read_csv('restaurants_clean.csv')
categories  = pd.read_csv('categories_clean.csv')
regions     = pd.read_csv('regions_clean.csv')
dishes      = pd.read_csv('dishes_clean.csv')

merged = restaurants.merge(
    categories[['category_id', 'category_name']], on='category_id', how='left'
).merge(
    regions[['zone_id', 'zone_name', 'area_name']].drop_duplicates('zone_id'),
    on='zone_id', how='left'
)

# Median price per restaurant from actual dish data
med_price = (
    dishes.groupby('restaurant_name')['price']
    .median()
    .reset_index()
    .rename(columns={'price': 'median_price'})
)
cluster_df = merged.merge(med_price, on='restaurant_name', how='left')

# ── Feature matrix & scaling ──────────────────────────────────
features   = ['rating', 'median_price']
X          = cluster_df[features].values
scaler     = StandardScaler()
X_scaled   = scaler.fit_transform(X)

# ── KMeans ───────────────────────────────────────────────────
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_df['cluster'] = kmeans.fit_predict(X_scaled)

# Map cluster IDs to stable labels based on median price
#  (so the colours stay consistent regardless of random init seed)
cluster_medians = (
    cluster_df.groupby('cluster')['median_price'].mean()
    .sort_values()
)
price_rank = {cid: rank for rank, cid in enumerate(cluster_medians.index)}
cluster_df['cluster_label'] = cluster_df['cluster'].map(price_rank)

label_map  = {0: 'Budget-Friendly Champions',
              1: 'Mid-Market Stars',
              2: 'Value Leaders'}
color_map  = {0: GREEN, 1: YELLOW, 2: ACCENT}

# Cluster centres back in original scale
centers_orig = scaler.inverse_transform(kmeans.cluster_centers_)

# ── Plot ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
ax.set_facecolor(CARD)

for cid in sorted(cluster_df['cluster_label'].unique()):
    sub   = cluster_df[cluster_df['cluster_label'] == cid]
    label = label_map[cid]
    color = color_map[cid]

    # Main scatter markers
    ax.scatter(
        sub['rating'], sub['median_price'],
        s=220, color=color,
        edgecolors='white', linewidth=1.2,
        label=label, zorder=5, alpha=0.9
    )

    # Annotate each point with restaurant name
    for _, row in sub.iterrows():
        ax.annotate(
            row['restaurant_name'],
            (row['rating'], row['median_price']),
            textcoords='offset points', xytext=(9, 6),
            fontsize=9, color=TEXT, fontweight='bold'
        )

# Soft ellipse "halos" around each cluster centre
for raw_cid, (cx, cy) in enumerate(centers_orig):
    ranked = price_rank[raw_cid]
    e = Ellipse(
        (cx, cy),
        width=0.25, height=65,
        color=color_map[ranked],
        alpha=0.08, zorder=1
    )
    ax.add_patch(e)

# ── Formatting ────────────────────────────────────────────────
ax.set_xlabel('Rating',               color=MUTED, fontsize=10)
ax.set_ylabel('Median Dish Price (EGP)', color=MUTED, fontsize=10)
ax.set_title(
    'K-Means Clustering: Rating vs Median Price  (k = 3)',
    color=TEXT, fontsize=13, fontweight='bold', pad=14
)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
ax.grid(True, color='#334155', linewidth=0.4, alpha=0.5)
ax.legend(
    facecolor=CARD, edgecolor='#334155',
    labelcolor=TEXT, fontsize=9,
    loc='upper left', framealpha=0.8
)

fig.text(
    0.5, 0.01,
    'Features standardised before clustering  |  KMeans random_state=42, n_init=10',
    ha='center', color=MUTED, fontsize=8.5
)

# ── Print cluster summary to console ──────────────────────────
print("\n── Cluster Summary ──────────────────────────────────────")
for cid in sorted(cluster_df['cluster_label'].unique()):
    sub = cluster_df[cluster_df['cluster_label'] == cid]
    print(f"\n{label_map[cid]}")
    print(f"  Members      : {list(sub['restaurant_name'])}")
    print(f"  Avg rating   : {sub['rating'].mean():.3f}")
    print(f"  Avg med price: EGP {sub['median_price'].mean():.0f}")

plt.tight_layout()
plt.savefig('10_kmeans.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("\nSaved → 10_kmeans.png")
