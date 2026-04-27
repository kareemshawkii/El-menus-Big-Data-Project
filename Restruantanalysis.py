# ================================
# Restaurant Analytics Dashboard
# Streamlit + Pandas + Numpy + Matplotlib Only
# Light Theme
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ================================
# Page Configuration
# ================================
st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# Color Palette (Light Theme)
# ================================
COLORS = {
    'PRIMARY': '#2E86AB',      # Primary Blue
    'SECONDARY': '#A23B72',    # Secondary Pink
    'SUCCESS': '#2E8B57',      # Green
    'WARNING': '#F18F01',      # Orange
    'DANGER': '#C73E1D',       # Red
    'INFO': '#1B998B',         # Teal
    'PURPLE': '#6B4E71',       # Purple
    'GOLD': '#FFB703',         # Yellow/Gold
    'LIGHT': '#F8F9FA',        # Light background
    'DARK': '#212529',         # Dark text
    'GRAY': '#6C757D',         # Gray text
    'WHITE': '#FFFFFF',        # White
    'BLUE_LIGHT': '#489FB5',
    'GREEN_LIGHT': '#80ED99',
    'RED_LIGHT': '#FF6B6B',
    'ORANGE_LIGHT': '#FFB347',
    'PALETTE': ['#2E86AB', '#A23B72', '#2E8B57', '#F18F01', '#6B4E71',
                '#1B998B', '#C73E1D', '#FFB703', '#489FB5', '#80ED99']
}

# ================================
# Load Data with Caching
# ================================
@st.cache_data
def load_data():
    try:
        restaurants = pd.read_csv('restaurants_clean.csv')
        categories = pd.read_csv('categories_clean.csv')
        regions = pd.read_csv('regions_clean.csv')
        dishes = pd.read_csv('dishes_clean.csv')
        
        # Merge datasets
        merged = restaurants.merge(
            categories[['category_id', 'category_name']], on='category_id', how='left'
        ).merge(
            regions[['zone_id', 'zone_name', 'area_name']].drop_duplicates('zone_id'),
            on='zone_id', how='left'
        )
        
        # Calculate median price per restaurant from dishes
        median_price = dishes.groupby('restaurant_name')['price'].median().reset_index()
        median_price.columns = ['restaurant_name', 'median_price']
        merged = merged.merge(median_price, on='restaurant_name', how='left')
        
        return restaurants, categories, regions, dishes, merged
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Load all data
with st.spinner("Loading data..."):
    restaurants, categories, regions, dishes, merged = load_data()

# ================================
# Helper Functions
# ================================
def apply_light_theme(fig, ax):
    """Apply light theme to matplotlib figures"""
    fig.patch.set_facecolor(COLORS['WHITE'])
    ax.set_facecolor(COLORS['LIGHT'])
    ax.tick_params(colors=COLORS['GRAY'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['GRAY'])
    ax.spines['bottom'].set_color(COLORS['GRAY'])
    return fig, ax

# ================================
# Sidebar Navigation
# ================================
st.sidebar.title("🍽️ Navigation")
page = st.sidebar.selectbox(
    "Select Dashboard Page",
    ["🏠 Overview Dashboard",
     "📊 Ratings Analysis",
     "💰 Price Analysis",
     "📍 Geographic Analysis",
     "📈 Statistical Insights",
     "🔍 Data Explorer"]
)

# KPIs in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Key Metrics")
st.sidebar.metric("Total Restaurants", len(restaurants))
st.sidebar.metric("Total Dishes", len(dishes))
st.sidebar.metric("Avg Rating", f"{restaurants['rating'].mean():.2f}")
st.sidebar.metric("Avg Price", f"${dishes['price'].mean():.2f}")

# ================================
# Page 1: Overview Dashboard
# ================================
if page == "🏠 Overview Dashboard":
    st.title("🍕 Restaurant Analytics Dashboard")
    st.markdown("---")
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏪 Total Restaurants", f"{len(restaurants):,}")
    with col2:
        st.metric("🍽️ Total Dishes", f"{len(dishes):,}")
    with col3:
        st.metric("⭐ Average Rating", f"{restaurants['rating'].mean():.2f}")
    with col4:
        st.metric("💰 Avg Dish Price", f"${dishes['price'].mean():.2f}")
    
    st.markdown("---")
    
    # Chart 1: Restaurant Ratings Horizontal Bar
    st.subheader("🏆 Restaurant Ratings Comparison")
    df_ratings = merged.sort_values('rating', ascending=True)
    bar_colors = [COLORS['SUCCESS'] if r >= 4.5 else COLORS['WARNING'] if r >= 4.3 else COLORS['DANGER'] 
                  for r in df_ratings['rating']]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig, ax = apply_light_theme(fig, ax)
    
    bars = ax.barh(df_ratings['restaurant_name'], df_ratings['rating'], 
                   color=bar_colors, height=0.6)
    
    for bar, val in zip(bars, df_ratings['rating']):
        ax.text(val + 0.003, bar.get_y() + bar.get_height()/2, 
                f'{val:.2f}', va='center', ha='left', 
                color=COLORS['DARK'], fontweight='bold', fontsize=9)
    
    ax.axvline(4.5, color=COLORS['PRIMARY'], linestyle='--', alpha=0.7, linewidth=1.5, label='Elite (4.5+)')
    ax.set_xlim(4.0, 4.85)
    ax.set_xlabel('Rating', fontsize=10)
    ax.set_title('Restaurant Ratings', fontweight='bold', fontsize=14)
    ax.legend(loc='lower right')
    
    st.pyplot(fig)
    plt.close()
    
    # Chart 2: Top Food Categories
    st.subheader("📂 Top Food Categories")
    top15 = categories.sort_values('restaurants_count', ascending=True).tail(15)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig, ax = apply_light_theme(fig, ax)
    
    bars = ax.barh(top15['category_name'], top15['restaurants_count'],
                   color=COLORS['PALETTE'][:len(top15)])
    
    for bar, val in zip(bars, top15['restaurants_count']):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2, str(val),
                va='center', ha='left', color=COLORS['DARK'], fontweight='bold')
    
    ax.set_xlabel('Number of Restaurants')
    ax.set_title('Top 15 Food Categories by Restaurant Count', fontweight='bold')
    st.pyplot(fig)
    plt.close()

# ================================
# Page 2: Ratings Analysis
# ================================
elif page == "📊 Ratings Analysis":
    st.title("⭐ Ratings Analysis")
    st.markdown("---")
    
    # Chart 3: Reviews vs Rating Bubble Chart
    st.subheader("💬 Reviews vs Rating (Bubble size = Number of Menu Items)")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    fig, ax = apply_light_theme(fig, ax)
    
    for i, (_, row) in enumerate(merged.iterrows()):
        bubble_size = row['num_dishes'] * 8
        ax.scatter(row['rating'], row['num_reviews']/1000, s=bubble_size,
                   color=COLORS['PALETTE'][i % len(COLORS['PALETTE'])],
                   alpha=0.6, edgecolors=COLORS['DARK'], linewidth=0.8)
        ax.annotate(row['restaurant_name'], (row['rating'], row['num_reviews']/1000),
                   xytext=(9, 5), textcoords='offset points',
                   fontsize=8, fontweight='bold')
    
    ax.set_xlabel('Rating', fontsize=11)
    ax.set_ylabel('Reviews (thousands)', fontsize=11)
    ax.set_title('Reviews vs Rating Analysis', fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()
    
    # Chart 4: Rating Distribution Histogram
    st.subheader("📊 Rating Distribution")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig, ax = apply_light_theme(fig, ax)
    
    counts, bins, patches = ax.hist(restaurants['rating'], bins=15, 
                                     color=COLORS['PRIMARY'], alpha=0.7, 
                                     edgecolor=COLORS['DARK'], linewidth=1.5)
    
    # Add value labels on bars
    for count, patch in zip(counts, patches):
        if count > 0:
            ax.text(patch.get_x() + patch.get_width()/2, count + 0.3, 
                   f'{int(count)}', ha='center', va='bottom', 
                   fontweight='bold')
    
    ax.set_xlabel('Rating', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title('Distribution of Restaurant Ratings', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()

# ================================
# Page 3: Price Analysis
# ================================
elif page == "💰 Price Analysis":
    st.title("💰 Price Analysis")
    st.markdown("---")
    
    # Chart 5: Average Price by Restaurant
    st.subheader("💵 Average Menu Price by Restaurant")
    df_price = merged.sort_values('avg_price', ascending=False).head(15)
    
    fig, ax = plt.subplots(figsize=(13, 6))
    fig, ax = apply_light_theme(fig, ax)
    
    bars = ax.bar(range(len(df_price)), df_price['avg_price'],
                  color=COLORS['PALETTE'][:len(df_price)], width=0.7)
    
    ax.set_xticks(range(len(df_price)))
    ax.set_xticklabels(df_price['restaurant_name'], rotation=45, ha='right')
    
    for bar, val in zip(bars, df_price['avg_price']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${val:.0f}', ha='center', va='bottom',
                fontweight='bold', fontsize=9)
    
    ax.set_ylabel('Average Price ($)', fontsize=11)
    ax.set_title('Top 15 Restaurants by Average Price', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()
    
    # Chart 6: Price Distribution Box Plot
    st.subheader("📦 Price Distribution by Restaurant")
    
    # Get top 10 restaurants by median price
    top_restaurants = dishes.groupby('restaurant_name')['price'].median().nlargest(10).index
    
    fig, ax = plt.subplots(figsize=(14, 7))
    fig, ax = apply_light_theme(fig, ax)
    
    # Create box plots
    data_to_plot = [dishes[dishes['restaurant_name'] == r]['price'].values for r in top_restaurants]
    bp = ax.boxplot(data_to_plot, labels=top_restaurants, patch_artist=True,
                    widths=0.6, showmeans=True, meanline=True)
    
    # Style the box plots
    for patch in bp['boxes']:
        patch.set_facecolor(COLORS['INFO'])
        patch.set_alpha(0.7)
        patch.set_edgecolor(COLORS['DARK'])
    
    for median in bp['medians']:
        median.set_color(COLORS['DANGER'])
        median.set_linewidth(2)
    
    for mean in bp['means']:
        mean.set_color(COLORS['PRIMARY'])
        mean.set_linewidth(2)
    
    ax.set_xticklabels(top_restaurants, rotation=45, ha='right')
    ax.set_ylabel('Price ($)', fontsize=11)
    ax.set_title('Price Distribution - Top 10 Restaurants by Median Price', 
                 fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()
    
    # Chart 7: Price Diversity Scatter
    st.subheader("🎯 Price Diversity Analysis")
    
    fig, ax = plt.subplots(figsize=(11, 7))
    fig, ax = apply_light_theme(fig, ax)
    
    for i, (_, row) in enumerate(merged.iterrows()):
        if pd.notna(row['price_std_dev']):
            bubble_size = (row['num_reviews'] / 3000) + 50
            ax.scatter(row['avg_price'], row['price_std_dev'], s=bubble_size,
                       color=COLORS['PALETTE'][i % len(COLORS['PALETTE'])],
                       alpha=0.6, edgecolors=COLORS['DARK'], linewidth=1)
            ax.annotate(row['restaurant_name'], (row['avg_price'], row['price_std_dev']),
                       xytext=(7, 5), textcoords='offset points',
                       fontsize=8, fontweight='bold')
    
    # Add median lines
    med_price = merged['avg_price'].median()
    med_std = merged['price_std_dev'].median()
    ax.axvline(med_price, color=COLORS['GRAY'], linestyle='--', alpha=0.7, linewidth=1.5)
    ax.axhline(med_std, color=COLORS['GRAY'], linestyle=':', alpha=0.7, linewidth=1.5)
    
    ax.set_xlabel('Average Price ($)', fontsize=11)
    ax.set_ylabel('Price Standard Deviation ($)', fontsize=11)
    ax.set_title('Price Diversity: Average Price vs Price Variation', 
                 fontweight='bold', fontsize=14)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()

# ================================
# Page 4: Geographic Analysis
# ================================
elif page == "📍 Geographic Analysis":
    st.title("📍 Geographic Analysis")
    st.markdown("---")
    
    # Chart 8: Top Areas by Delivery Zones
    st.subheader("🗺️ Top Areas by Delivery Zone Coverage")
    
    area_zone_count = regions.groupby('area_name')['zone_id'].count().sort_values(ascending=True).tail(20)
    
    fig, ax = plt.subplots(figsize=(13, 9))
    fig, ax = apply_light_theme(fig, ax)
    
    bars = ax.barh(range(len(area_zone_count)), area_zone_count.values,
                   color=COLORS['PALETTE'])
    
    ax.set_yticks(range(len(area_zone_count)))
    ax.set_yticklabels(area_zone_count.index)
    
    for bar, val in zip(bars, area_zone_count.values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, str(val),
                va='center', ha='left', fontweight='bold')
    
    ax.set_xlabel('Number of Delivery Zones', fontsize=11)
    ax.set_title('Top 20 Areas by Delivery Zone Coverage', fontweight='bold', fontsize=14)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()
    
    # Chart 9: Category Distribution Pie Chart
    st.subheader("🥧 Category Distribution")
    
    top_categories = categories.nlargest(8, 'restaurants_count')
    other_sum = categories['restaurants_count'].sum() - top_categories['restaurants_count'].sum()
    
    if other_sum > 0:
        categories_for_pie = pd.concat([top_categories, pd.DataFrame({'category_name': ['Other'], 'restaurants_count': [other_sum]})])
    else:
        categories_for_pie = top_categories
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig, ax = apply_light_theme(fig, ax)
    
    wedges, texts, autotexts = ax.pie(categories_for_pie['restaurants_count'], 
                                       labels=categories_for_pie['category_name'],
                                       autopct='%1.1f%%',
                                       colors=COLORS['PALETTE'],
                                       startangle=90)
    
    for text in texts:
        text.set_fontsize(9)
        text.set_fontweight('bold')
    for autotext in autotexts:
        autotext.set_color(COLORS['WHITE'])
        autotext.set_fontweight('bold')
        autotext.set_fontsize(8)
    
    ax.set_title('Restaurant Distribution by Category', fontweight='bold', fontsize=14, pad=20)
    
    st.pyplot(fig)
    plt.close()

# ================================
# Page 5: Statistical Insights
# ================================
elif page == "📈 Statistical Insights":
    st.title("📈 Statistical Insights")
    st.markdown("---")
    
    # Chart 10: Rating vs Price Scatter with Trend Line
    st.subheader("📉 Rating vs Average Price Correlation")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    fig, ax = apply_light_theme(fig, ax)
    
    # Scatter plot
    ax.scatter(merged['avg_price'], merged['rating'], 
              alpha=0.7, s=100, c=COLORS['PRIMARY'], 
              edgecolors=COLORS['DARK'], linewidth=1.5)
    
    # Add trend line
    x = merged['avg_price'].dropna().values
    y = merged['rating'].dropna().values
    
    if len(x) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(x.min(), x.max(), 100)
        ax.plot(x_trend, p(x_trend), color=COLORS['DANGER'], linestyle='--', 
               linewidth=2, label=f'Trend (slope: {z[0]:.3f})')
    
    # Annotate some points
    for _, row in merged.head(8).iterrows():
        ax.annotate(row['restaurant_name'], (row['avg_price'], row['rating']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8)
    
    ax.set_xlabel('Average Price ($)', fontsize=11)
    ax.set_ylabel('Rating', fontsize=11)
    ax.set_title('Rating vs Average Price with Trend Line', fontweight='bold', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3, linestyle='--')
    
    st.pyplot(fig)
    plt.close()
    
    # Statistical Summary Tables
    st.subheader("📊 Statistical Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Restaurants Statistics**")
        st.dataframe(restaurants[['rating', 'num_reviews', 'num_dishes', 'avg_price']].describe(), 
                    use_container_width=True)
    
    with col2:
        st.markdown("**Dishes Statistics**")
        st.dataframe(dishes[['price']].describe(), use_container_width=True)
    
    # Correlation Matrix
    st.subheader("📈 Correlation Matrix")
    
    numeric_cols = ['rating', 'num_reviews', 'num_dishes', 'avg_price']
    if 'price_std_dev' in merged.columns:
        numeric_cols.append('price_std_dev')
    
    corr_matrix = merged[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    fig, ax = apply_light_theme(fig, ax)
    
    # Create heatmap
    im = ax.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    
    # Add text annotations
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            text_color = 'white' if abs(corr_matrix.iloc[i, j]) > 0.5 else COLORS['DARK']
            text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                          ha="center", va="center", 
                          color=text_color,
                          fontweight='bold', fontsize=10)
    
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
    ax.set_yticklabels(numeric_cols)
    ax.set_title('Feature Correlation Matrix', fontweight='bold', pad=20)
    
    # Add colorbar
    plt.colorbar(im, ax=ax)
    
    st.pyplot(fig)
    plt.close()

# ================================
# Page 6: Data Explorer
# ================================
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏪 Restaurants", "🍽️ Dishes", "📂 Categories", "📍 Regions"])
    
    with tab1:
        st.subheader("Restaurants Data")
        search = st.text_input("🔍 Search restaurant:", "")
        if search:
            filtered = restaurants[restaurants['restaurant_name'].str.contains(search, case=False)]
        else:
            filtered = restaurants
        st.dataframe(filtered, use_container_width=True)
        st.caption(f"Showing {len(filtered)} of {len(restaurants)} restaurants")
        
    with tab2:
        st.subheader("Dishes Data")
        col1, col2 = st.columns(2)
        with col1:
            restaurant_filter = st.selectbox("Filter by restaurant:", ["All"] + sorted(dishes['restaurant_name'].unique().tolist()))
        with col2:
            max_price = st.slider("Max price:", 0, int(dishes['price'].max()), int(dishes['price'].max()))
        
        if restaurant_filter != "All":
            filtered = dishes[dishes['restaurant_name'] == restaurant_filter]
        else:
            filtered = dishes
        
        filtered = filtered[filtered['price'] <= max_price]
        st.dataframe(filtered, use_container_width=True)
        st.caption(f"Showing {len(filtered)} of {len(dishes)} dishes")
        
    with tab3:
        st.subheader("Categories Data")
        st.dataframe(categories, use_container_width=True)
        
    with tab4:
        st.subheader("Regions Data")
        area_filter = st.selectbox("Filter by area:", ["All"] + sorted(regions['area_name'].unique().tolist()))
        if area_filter != "All":
            filtered = regions[regions['area_name'] == area_filter]
        else:
            filtered = regions
        st.dataframe(filtered, use_container_width=True)
        st.caption(f"Showing {len(filtered)} of {len(regions)} regions")

# ================================
# Footer and Export
# ================================
st.markdown("---")
st.markdown("✅ **Dashboard Ready** | Built with Streamlit, Pandas, NumPy & Matplotlib")

# Export functionality
st.sidebar.markdown("---")
if st.sidebar.button("📥 Export Analysis Results"):
    avg_price_per_rest = dishes.groupby('restaurant_name')['price'].mean().sort_values(ascending=False)
    avg_price_per_rest.to_csv("avg_price_per_restaurants.csv")
    st.sidebar.success("✅ Results exported to CSV!")