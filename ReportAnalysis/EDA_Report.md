# 🍔 Food & Restaurant Ecosystem — Comprehensive EDA Report

> **Analyst:** Senior Data Analyst & ML Expert  
> **Phase:** Exploratory Data Analysis & Insight Generation  
> **Datasets:** restaurants_clean · regions_clean · dishes_clean · categories_clean

---

## 1. Data Understanding

### 1.1 Dataset Overview

| Dataset | Rows | Columns | Description |
|---|---|---|---|
| `restaurants_clean` | 10 | 11 | Restaurant profiles with performance KPIs |
| `regions_clean` | 1,141 | 4 | Geographic hierarchy: zones → areas |
| `dishes_clean` | 310 | 6 | Individual menu items with prices |
| `categories_clean` | 26 | 3 | Food categories and their market size |

### 1.2 Column Descriptions

#### `restaurants_clean`
| Column | Type | Meaning |
|---|---|---|
| `restaurant_id` | UUID | Primary key |
| `restaurant_name` | str | Brand name |
| `branch_code` | str | Unique branch identifier |
| `zone_id` | UUID | FK → regions.zone_id |
| `category_id` | UUID | FK → categories.category_id |
| `rating` | float | Aggregate customer rating (1–5) |
| `num_reviews` | int | Total review count (proxy for popularity) |
| `num_dishes` | int | Number of menu items |
| `avg_price` | float | Mean price across all dishes (EGP) |
| `price_variance` | float | Price spread — measures menu diversity |
| `price_std_dev` | float | Standard deviation of dish prices |

#### `regions_clean`
| Column | Meaning |
|---|---|
| `zone_id` | Granular delivery zone (FK to restaurants) |
| `zone_name` | Human-readable zone label |
| `area_id` | Parent area grouping |
| `area_name` | Neighborhood / district name |

#### `dishes_clean`
| Column | Meaning |
|---|---|
| `restaurant_id` / `restaurant_name` | Parent restaurant |
| `menu_section` | Menu category (Chicken, Beverages, etc.) |
| `dish_name` | Item name |
| `size_name` | Portion variant (Regular, Large, etc.) |
| `price` | Item price in EGP |

#### `categories_clean`
| Column | Meaning |
|---|---|
| `category_id` | Primary key |
| `category_name` | Food category label |
| `restaurants_count` | Number of restaurants in this category |

### 1.3 Key Relationships

```
categories ──── category_id ────▶ restaurants ◀──── zone_id ──── regions
                                       │
                                  restaurant_id
                                       │
                                       ▼
                                    dishes
```

---

## 2. Data Integration (Joins)

```python
# Join 1: Restaurants ← Categories (category dimension)
merged = restaurants.merge(
    categories[['category_id', 'category_name']],
    on='category_id', how='left'
)

# Join 2: Merged ← Regions (geographic dimension)
merged = merged.merge(
    regions[['zone_id', 'zone_name', 'area_name']].drop_duplicates('zone_id'),
    on='zone_id', how='left'
)

# Join 3: Dishes ← Restaurant metadata (for enriched dish analysis)
dishes_full = dishes.merge(
    restaurants[['restaurant_id', 'rating', 'category_id']],
    on='restaurant_id', how='left'
).merge(
    categories[['category_id', 'category_name']],
    on='category_id', how='left'
)
```

**Observation:** All 10 restaurants belong to the **Burgers** category and are located in the **Abbas El Akkad** zone (Nasr City 3 area). This indicates the dataset is a focused competitive analysis of the Nasr City burger segment.

---

## 3. Exploratory Data Analysis

### 3.1 Univariate Analysis — Restaurants

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

restaurants = pd.read_csv('restaurants_clean.csv')
print(restaurants[['rating','num_reviews','num_dishes','avg_price','price_std_dev']].describe())
```

| Metric | Min | Median | Mean | Max |
|---|---|---|---|---|
| Rating | 4.20 | 4.49 | 4.47 | 4.68 |
| Reviews | 3,600 | 53,823 | 73,746 | 266,406 |
| Menu Items | 4 | 14 | 30.3 | 203 |
| Avg Price (EGP) | 66.00 | 207.50 | 206.54 | 333.30 |
| Price Std Dev | 4.30 | 53.52 | 74.35 | 235.68 |

**Key observations:**
- Rating range is narrow (4.20–4.68) — all restaurants are above average, suggesting strong market selection in this zone
- Review counts are heavily right-skewed (mean 73K >> median 54K), driven by McDonald's massive 266K reviews
- Menu size varies from 4 items (GAD) to 203 items (McDonald's) — a 50x difference

### 3.2 Univariate Analysis — Categories

```python
categories.sort_values('restaurants_count', ascending=False).head(10)
```

| Rank | Category | Restaurant Count |
|---|---|---|
| 1 | Desserts | 222 |
| 2 | Salads | 220 |
| 3 | Sandwiches | 212 |
| 4 | Grilled Chicken | 155 |
| 5 | Fried Chicken | 150 |
| 6 | Pasta | 133 |
| 7 | Seafood | 113 |
| 8 | Burgers | 113 |
| 9 | Grills | 109 |
| 10 | Coffee | 92 |

### 3.3 Univariate Analysis — Dishes

```python
print(dishes['price'].describe())
print(dishes['menu_section'].value_counts().head(5))
```

- **Price range:** EGP 25 – 1,260 (mean: 188, median: 184)
- **Top menu sections:** Chicken (52 items), Beverages (45), Breakfast (33), Beef (31)
- **Size variants:** Regular most common (72 items), then Sandwich (39), then LARGE_MEAL / MEDIUM_MEAL (25 each)

### 3.4 Univariate Analysis — Regions

```python
regions.groupby('area_name')['zone_id'].count().sort_values(ascending=False).head(5)
```

| Area | Delivery Zones |
|---|---|
| New Cairo | 178 |
| 6th of October | 59 |
| Haram and Faisal | 54 |
| Maadi | 53 |
| Nasr City | 44 |

---

## 4. Visualizations & Business Insights

---

### Chart 1 — Restaurant Ratings Comparison

![Ratings Bar Chart](charts/01_ratings.png)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(13, 6), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

df_sorted = merged.sort_values('rating', ascending=True)
colors = ['#22C55E' if r >= 4.5 else '#FACC15' if r >= 4.3 else '#EF4444'
          for r in df_sorted['rating']]

bars = ax.barh(df_sorted['restaurant_name'], df_sorted['rating'],
               color=colors, edgecolor='none', height=0.6)

for bar, val in zip(bars, df_sorted['rating']):
    ax.text(val + 0.003, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}', va='center', ha='left', color='white', fontsize=10, fontweight='bold')

ax.set_xlim(4.0, 4.85)
ax.axvline(4.5, color='#38BDF8', linestyle='--', linewidth=1.2, alpha=0.7, label='4.5 threshold')
ax.legend(facecolor='#1E293B', edgecolor='none', labelcolor='white', fontsize=9)
ax.set_title('★  Restaurant Ratings Comparison', color='white', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('01_ratings.png', dpi=150, bbox_inches='tight', facecolor='#0F172A')
```

**Interpretation:** Buffalo Burger leads with a rating of **4.68**, followed closely by McDonald's (4.65) and Butcher's Burger (4.62). Munch & Shake and Cook Door trail behind with ratings below 4.35.

**Business Insight:** The top 5 restaurants (≥4.5 rating) represent the **"Elite Tier"** of this competitive market. Munch & Shake and Cook Door need a quality or experience improvement strategy to compete at the same level.

---

### Chart 2 — Reviews vs Rating (Bubble = Menu Size)

![Bubble Chart](charts/02_reviews_vs_rating.png)

```python
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

for i, (_, row) in enumerate(merged.iterrows()):
    ax.scatter(row['rating'], row['num_reviews'] / 1000,
               s=row['num_dishes'] * 8, color=PALETTE[i],
               alpha=0.85, edgecolors='white', linewidth=0.6, zorder=5)
    ax.annotate(row['restaurant_name'], (row['rating'], row['num_reviews'] / 1000),
                textcoords='offset points', xytext=(8, 4),
                fontsize=8.5, color='white', fontweight='bold')

ax.set_xlabel('Rating')
ax.set_ylabel('Reviews (thousands)')
ax.set_title('Reviews vs Rating  (bubble = # of menu items)', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('02_reviews_vs_rating.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** McDonald's occupies a unique quadrant — top-3 rating AND the highest review count (266K) by a massive margin, combined with a very large bubble (203 menu items). Bazooka is a hidden gem: 154K reviews but only 15 dishes and a moderate rating.

**Business Insight:** Reach ≠ Rating. Bazooka has strong customer engagement with a small menu, suggesting menu focus over breadth can still drive traffic. Restaurants like Munch & Shake and Cook Door have relatively low reviews and lower ratings — they need marketing investment.

---

### Chart 3 — Average Menu Price by Restaurant

![Price Bar Chart](charts/03_avg_price.png)

```python
fig, ax = plt.subplots(figsize=(13, 6), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

df_p = merged.sort_values('avg_price', ascending=False)
bars = ax.bar(df_p['restaurant_name'], df_p['avg_price'],
              color=PALETTE[:len(df_p)], edgecolor='none', width=0.6)

for bar, val in zip(bars, df_p['avg_price']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
            f'EGP {val:.0f}', ha='center', va='bottom', color='white',
            fontsize=9, fontweight='bold')

ax.set_xticklabels(df_p['restaurant_name'], rotation=30, ha='right', color='white')
ax.set_title('Average Menu Price by Restaurant', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('03_avg_price.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** Buffalo Burger (EGP 333) is the most premium brand in this cluster, nearly 5x more expensive than GAD (EGP 66). McDonald's (EGP 164) and Prego (EGP 147) are the affordable options relative to their peers.

**Business Insight:** **GAD** at EGP 66 is operating in the extreme budget segment. If its rating (4.48) holds, it could be a value leader. Buffalo Burger commands a premium — its high rating justifies this positioning and attracts quality-conscious consumers.

---

### Chart 4 — Price Distribution per Restaurant (Violin + Strip)

![Violin Chart](charts/04_price_violin.png)

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

order = dishes.groupby('restaurant_name')['price'].median().sort_values(ascending=False).index

sns.violinplot(data=dishes, x='restaurant_name', y='price', order=order,
               palette=PALETTE, inner=None, ax=ax, cut=0)
sns.stripplot(data=dishes, x='restaurant_name', y='price', order=order,
              color='white', alpha=0.5, size=3.5, jitter=True, ax=ax)

ax.set_xticklabels(order, rotation=35, ha='right', color='white')
ax.set_title('Price Distribution per Restaurant', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('04_price_violin.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** Buffalo Burger shows the widest price spread (wide violin), indicating a menu that spans from entry-level to premium options. McDonald's has a large distribution too but with outliers in the high-price bundle meals. GAD and Prego are tightly clustered, reflecting simple, consistent menus.

**Business Insight:** High price variance (Buffalo Burger, Bazooka) is a deliberate upselling strategy — offering something for everyone. Narrow distributions (GAD, Munch & Shake) signal operational simplicity and a focused customer base.

---

### Chart 5 — Top 15 Food Categories by Restaurant Count

![Category Market](charts/05_category_market.png)

```python
fig, ax = plt.subplots(figsize=(13, 8), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

top_cats = categories.sort_values('restaurants_count', ascending=True).tail(15)
bars = ax.barh(top_cats['category_name'], top_cats['restaurants_count'],
               color=PALETTE * 3, edgecolor='none', height=0.65)

for bar, val in zip(bars, top_cats['restaurants_count']):
    ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
            str(val), va='center', ha='left', color='white', fontsize=9)

ax.set_title('Top 15 Food Categories by Restaurant Count', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('05_category_market.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** Desserts (222), Salads (220), and Sandwiches (212) are the most saturated categories. Koshary (8), Donuts (12), and Shareables (13) are the least contested.

**Business Insight:** 
- **Overcrowded markets**: Desserts, Salads, and Sandwiches — entering these requires a strong differentiation
- **Blue ocean opportunities**: Koshary (niche, culturally loved), Donuts, Waffles, and Pancakes are dramatically under-served relative to their consumer demand
- Burgers (113) and Grills (109) — the dataset's focus — are in the mid-tier by count

---

### Chart 6 — Top 20 Areas by Delivery Zone Coverage

![Regions Chart](charts/06_regions.png)

```python
area_counts = regions.groupby('area_name')['zone_id'].count().sort_values(ascending=True).tail(20)

fig, ax = plt.subplots(figsize=(13, 9), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

bars = ax.barh(area_counts.index, area_counts.values,
               color=PALETTE * 4, edgecolor='none', height=0.65)

ax.set_title('Top 20 Areas by Delivery Zone Coverage', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('06_regions.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** New Cairo dominates with 178 delivery zones — nearly 3x more than its nearest competitors (6th of October: 59, Haram & Faisal: 54). Maadi, Nasr City, and Heliopolis round out the top 5.

**Business Insight:** New Cairo's massive zone count reflects rapid urban growth and high restaurant demand. Any new restaurant chain's **expansion priority should be New Cairo first**, followed by 6th of October and Maadi. Smaller areas like Al Mokatam (7 zones) and Downtown (10) may be underserved.

---

### Chart 7 — Menu Section Composition (Donut)

![Menu Donut](charts/07_menu_donut.png)

```python
import matplotlib.pyplot as plt

sec_counts = dishes['menu_section'].value_counts()
major = sec_counts[sec_counts >= 6]
other = pd.Series({'Other': sec_counts[sec_counts < 6].sum()})
sec_plot = pd.concat([major, other]).sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0F172A')
wedges, texts, autotexts = ax.pie(
    sec_plot.values, labels=sec_plot.index,
    autopct='%1.1f%%', startangle=140,
    colors=PALETTE, wedgeprops=dict(width=0.55, edgecolor='#0F172A', linewidth=2)
)
ax.set_title('Menu Section Composition', color='white', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('07_menu_donut.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** Chicken (16.8%) is the single biggest menu section, followed by Beverages (14.5%) and Breakfast (10.6%). Beef items (10%) are also strong. Together, Chicken + Beef + Breakfast account for ~37% of all dish slots.

**Business Insight:** Beverages are the second-largest category — they're high-margin add-ons. Restaurants should ensure a strong beverage menu alongside their main dishes to maximize revenue per order.

---

### Chart 8 — Feature Correlation Heatmap

![Heatmap](charts/08_heatmap.png)

```python
import seaborn as sns
import numpy as np

num_cols = ['rating', 'num_reviews', 'num_dishes', 'avg_price', 'price_variance', 'price_std_dev']
corr = merged[num_cols].corr()

fig, ax = plt.subplots(figsize=(9, 7), facecolor='#0F172A')
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, annot=True, fmt='.2f', cmap=cmap,
            xticklabels=['Rating','Reviews','# Dishes','Avg Price','Price Var','Price Std'],
            yticklabels=['Rating','Reviews','# Dishes','Avg Price','Price Var','Price Std'],
            ax=ax, linewidths=0.5)
ax.set_title('Feature Correlation Heatmap', color='white', fontsize=13)
plt.tight_layout()
plt.savefig('08_heatmap.png', dpi=150, bbox_inches='tight')
```

**Interpretation & Correlations:**

| Pair | Correlation | Meaning |
|---|---|---|
| Rating ↔ Reviews | +0.46 | Higher-rated restaurants tend to attract more reviews |
| Avg Price ↔ Price Std Dev | **+0.96** | Very strong — higher average price = more price spread |
| Avg Price ↔ Price Variance | **+0.96** | Same — price and menu diversity move together |
| Num Dishes ↔ Reviews | +0.39 | Larger menus correlate with more customer engagement |
| Rating ↔ Avg Price | -0.12 | Slight negative — premium price does not guarantee better rating |

**Business Insight:** Price and price diversity are almost perfectly correlated — restaurants that charge more tend to have a wider price range (bundling low-cost and premium items). Importantly, **higher average price does not translate to better ratings**, disproving the "premium = quality perception" assumption in this market.

---

### Chart 9 — Price Diversity: Avg Price vs Price Std Dev

![Price Diversity](charts/09_price_diversity.png)

```python
fig, ax = plt.subplots(figsize=(11, 7), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

for i, (_, row) in enumerate(merged.iterrows()):
    ax.scatter(row['avg_price'], row['price_std_dev'],
               s=row['num_reviews'] / 3000, color=PALETTE[i],
               alpha=0.85, edgecolors='white', linewidth=0.5, zorder=5)
    ax.annotate(row['restaurant_name'], (row['avg_price'], row['price_std_dev']),
                textcoords='offset points', xytext=(6, 4), fontsize=8, color='white')

ax.set_xlabel('Average Price (EGP)')
ax.set_ylabel('Price Std Deviation (EGP)')
ax.set_title('Price Diversity: Avg Price vs Price Std Dev (bubble = review volume)', color='white')
plt.tight_layout()
plt.savefig('09_price_diversity.png', dpi=150, bbox_inches='tight')
```

**Interpretation:** Buffalo Burger stands out as both the most expensive AND most price-diverse restaurant. GAD is the opposite: low price, ultra-low variance (only EGP 4.30 std dev!). McDonald's has a large bubble (review volume) with moderate price diversity.

**Business Insight:** Restaurants with high price diversity (Buffalo Burger, Bazooka) are practicing **good-better-best pricing** — capturing multiple wallet sizes. GAD's single-price strategy works in a niche budget market. Restaurants in the middle (Burger King, Cook Door) may benefit from introducing either premium upgrades or value bundles.

---

### Chart 10 — K-Means Clustering (Rating × Median Price, k=3)

![K-Means](charts/10_kmeans.png)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

med_price = dishes.groupby('restaurant_name')['price'].median().reset_index()
med_price.columns = ['restaurant_name', 'median_price']
cluster_df = merged.merge(med_price, on='restaurant_name', how='left')

X = cluster_df[['rating', 'median_price']].values
X_scaled = StandardScaler().fit_transform(X)

cluster_df['cluster'] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X_scaled)

cluster_labels = {0: 'Budget Champions', 1: 'Mid-Market Stars', 2: 'Premium Players'}

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0F172A')
ax.set_facecolor('#1E293B')

for cid in cluster_df['cluster'].unique():
    sub = cluster_df[cluster_df['cluster'] == cid]
    ax.scatter(sub['rating'], sub['median_price'],
               s=220, label=cluster_labels[cid], edgecolors='white', linewidth=1.2)
    for _, row in sub.iterrows():
        ax.annotate(row['restaurant_name'], (row['rating'], row['median_price']),
                    textcoords='offset points', xytext=(8, 5), fontsize=9, color='white')

ax.set_xlabel('Rating')
ax.set_ylabel('Median Dish Price (EGP)')
ax.set_title('K-Means Clustering: Rating vs Median Price (k=3)', color='white', fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig('10_kmeans.png', dpi=150, bbox_inches='tight')
```

**Cluster Results:**

| Cluster | Members | Avg Rating | Avg Median Price |
|---|---|---|---|
| 🟢 Budget-Friendly Champions | Buffalo Burger, Butcher's Burger, Stack'd | **4.62** | EGP 251 |
| 🟡 Mid-Market Stars | Burger King, Bazooka, Munch & Shake, Cook Door | 4.30 | EGP 205 |
| 🔵 Value Leaders | McDonald's, Prego, GAD | 4.54 | EGP 109 |

**Business Insight:**
- **Budget-Friendly Champions** have high ratings despite mid-range prices — they deliver genuine quality. These are the market's most dangerous competitors.
- **Mid-Market Stars** have lower ratings despite similar/higher prices — a clear **value gap** that customers notice.
- **Value Leaders** (McDonald's, GAD) are the volume play — affordable and well-rated. McDonald's is unique in achieving both massive scale AND strong rating.

---

## 5. Business Insights Summary

### 🏆 Which restaurants perform best and why?

| Rank | Restaurant | Reason |
|---|---|---|
| 1 | **Buffalo Burger** | Highest rating (4.68), premium positioning, strong brand loyalty |
| 2 | **McDonald's** | Most reviews (266K), largest menu (203 items), solid rating (4.65), strong value positioning |
| 3 | **Butcher's Burger** | High rating (4.62), consistent pricing (low std dev) |

### 🔥 Most Popular Categories (by restaurant count)

1. **Desserts** (222 restaurants) — near-universal addition to menus
2. **Salads** (220) — growing health-consciousness
3. **Sandwiches** (212) — everyday staple

### 🗺 Highest Demand Regions

- **New Cairo** dominates with **178 delivery zones** — the #1 expansion target
- **6th of October** and **Maadi** follow as dense, commercially active areas

### 💡 Hidden Opportunities & Underserved Markets

| Opportunity | Evidence |
|---|---|
| **Koshary** | Only 8 restaurants in a beloved Egyptian staple category — massive cultural demand, minimal competition |
| **Donuts & Waffles** | 12 and 23 restaurants respectively — rising dessert trend with low supply |
| **Breakfast** category | Strong menu section in dishes (33 items) but only 69 breakfast-dedicated restaurants |
| **Downtown** area | Only 10 delivery zones for a central, high-footfall district |
| **GAD price model** | At EGP 66 avg with 4.48 rating — the value-for-money segment is underexplored |

---

## 6. Strategic Recommendations

### For Restaurant Owners
1. **Focus on quality over menu breadth** — Bazooka gets 154K reviews with just 15 dishes
2. **Adopt good-better-best pricing** to capture diverse wallet sizes (see Buffalo Burger)
3. **Improve review acquisition** — rating × review count creates a flywheel of trust
4. **Expand to New Cairo** — the coverage leaders in delivery zones will win more orders

### For Customers
- **Best value**: GAD (EGP 66 avg, 4.48 rating) or McDonald's for variety
- **Best quality**: Buffalo Burger (4.68 rating)
- **Best variety**: McDonald's (203 items across all meal occasions)

### For Business Stakeholders
1. **Invest in Koshary and Breakfast** — two high-demand, low-competition segments
2. **Develop New Cairo and 6th of October** delivery infrastructure first
3. **Target Desserts as an add-on vertical**, not a stand-alone business (222 restaurants already compete)
4. **Mid-Market Star restaurants** (Burger King, Cook Door) represent acquisition or partnership opportunities — strong brand recognition with room for quality improvement

---

*Report generated using Python · pandas · seaborn · matplotlib · scikit-learn*
