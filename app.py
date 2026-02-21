import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="NYC Taxi Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# TITLE AND INTRODUCTION
# ============================================================================
st.title("🚕 NYC Yellow Taxi Dashboard")
st.markdown("""
This interactive dashboard provides insights into NYC yellow taxi trips for January 2024.
Explore key metrics, visualize patterns, and filter data to discover trends in pick-up zones,
passenger behavior, payment methods, and temporal patterns.
""")

st.divider()

# ============================================================================
# DATA LOADING AND CACHING
# ============================================================================
@st.cache_data
def load_data():
    """Load and process taxi data"""
    try:
        df = pd.read_parquet('data/processed/taxi_summary.parquet')
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        df['pickup_date'] = df['date'].dt.date
        df['day_of_week'] = df['date'].dt.day_name()
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        
        # Calculate derived metrics
        df['avg_distance'] = df['total_distance'] / df['num_trips']
        df['avg_fare'] = df['total_fares'] / df['num_trips']
        df['avg_tip'] = df['total_tips'] / df['num_trips']
        df['avg_passengers'] = df['total_passengers'] / df['num_trips']
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None

# Load data
df = load_data()

if df is None:
    st.stop()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.header("🔧 Filters")

# Date range selector
min_date = df['pickup_date'].min()
max_date = df['pickup_date'].max()

# Set default range to 2024 only
default_start = pd.to_datetime('2024-01-01').date()
default_end = pd.to_datetime('2024-12-31').date()

# Adjust if data doesn't cover full year
if default_start < min_date:
    default_start = min_date
if default_end > max_date:
    default_end = max_date

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(default_start, default_end),
    min_value=min_date,
    max_value=max_date,
    key="date_range"
)

# Ensure date_range is a tuple
if not isinstance(date_range, tuple):
    date_range = (date_range, date_range)
elif len(date_range) == 1:
    date_range = (date_range[0], date_range[0])

# Hour range slider (0-23)
hour_range = st.sidebar.slider(
    "Select Hour Range:",
    min_value=0,
    max_value=23,
    value=(0, 23),
    key="hour_range"
)

# ============================================================================
# APPLY FILTERS
# ============================================================================
def apply_filters(data):
    """Apply all filters to the dataset"""
    filtered = data.copy()
    
    # Convert dates to same format for comparison
    start_date = pd.to_datetime(date_range[0]).date()
    end_date = pd.to_datetime(date_range[1]).date()
    
    # Apply date filter
    filtered = filtered[(filtered['pickup_date'] >= start_date) & 
                       (filtered['pickup_date'] <= end_date)]
    
    # Apply hour filter
    filtered = filtered[(filtered['hour'] >= hour_range[0]) & 
                       (filtered['hour'] <= hour_range[1])]
    
    return filtered

filtered_df = apply_filters(df)

st.sidebar.info(f"📊 Filtered Data: {len(filtered_df):,} records out of {len(df):,} total")

# ============================================================================
# KEY METRICS
# ============================================================================
st.header("📈 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_trips = filtered_df['num_trips'].sum()
    st.metric("Total Trips", f"{total_trips:,}")

with col2:
    avg_fare = filtered_df['avg_fare'].mean()
    st.metric("Avg Fare", f"${avg_fare:.2f}")

with col3:
    total_revenue = filtered_df['total_fares'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col4:
    avg_distance = filtered_df['avg_distance'].mean()
    st.metric("Avg Trip Distance", f"{avg_distance:.2f} miles")

with col5:
    total_tips = filtered_df['total_tips'].sum()
    st.metric("Total Tips", f"${total_tips:,.2f}")

st.divider()

# ============================================================================
# VISUALIZATIONS SECTION
# ============================================================================
st.header("📊 Visualizations")

# Create tabs for better organization
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Trips Over Time",
    "Fare Trends by Hour",
    "Trip Distance Analysis",
    "Tips Analysis",
    "Passenger Patterns"
])

# ============================================================================
# TAB 1: TRIPS OVER TIME (LINE CHART)
# ============================================================================
with tab1:
    st.subheader("1. Number of Trips Over Time")
    
    daily_trips = filtered_df.groupby('pickup_date')['num_trips'].sum().reset_index()
    daily_trips['date'] = pd.to_datetime(daily_trips['pickup_date'])
    
    fig_trips = px.line(
        daily_trips,
        x='date',
        y='num_trips',
        markers=True,
        title='Daily Trip Count',
        labels={'date': 'Date', 'num_trips': 'Number of Trips'},
        line_shape='spline'
    )
    fig_trips.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig_trips, use_container_width=True)
    
    st.markdown("""
    **Insights:**
    - The trip volume shows clear temporal patterns, with notable fluctuations throughout the period.
    - Weekend and weekday patterns are visible, with potential dips during certain periods.
    - The overall trend indicates consistent taxi usage with variations based on day of week and external factors.
    """)

# ============================================================================
# TAB 2: AVERAGE FARE BY HOUR (BAR CHART)
# ============================================================================
with tab2:
    st.subheader("2. Average Fare by Hour of Day")
    
    hourly_fare = filtered_df.groupby('hour')['avg_fare'].mean().reset_index()
    
    fig_hour = px.bar(
        hourly_fare,
        x='hour',
        y='avg_fare',
        title='Average Fare by Hour of Day',
        labels={'hour': 'Hour of Day (24H)', 'avg_fare': 'Average Fare ($)'},
        color='avg_fare',
        color_continuous_scale='Blues'
    )
    fig_hour.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_hour, use_container_width=True)
    
    st.markdown("""
    **Insights:**
    - Fares show distinct hourly patterns, with peak fares typically during high-demand periods.
    - Morning and evening rush hours generally command higher fares due to increased competition and demand.
    - Late night and early morning hours show more variable fare patterns reflecting different passenger demographics.
    """)

# ============================================================================
# TAB 3: AVERAGE TRIP DISTANCE (BAR CHART)
# ============================================================================
with tab3:
    st.subheader("3. Trip Distance Distribution by Hour")
    
    hourly_distance = filtered_df.groupby('hour')['avg_distance'].mean().reset_index()
    
    fig_dist = px.bar(
        hourly_distance,
        x='hour',
        y='avg_distance',
        title='Average Trip Distance by Hour',
        labels={'hour': 'Hour of Day (24H)', 'avg_distance': 'Average Distance (miles)'},
        color='avg_distance',
        color_continuous_scale='Viridis'
    )
    fig_dist.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_dist, use_container_width=True)
    
    st.markdown(f"""
    **Insights:**
    - Average trip distance varies by time of day, with some hours showing longer typical trips than others.
    - Off-peak hours may include more airport trips and longer-distance journeys, affecting average distance.
    - Peak hours tend to have shorter average trips reflecting urban commuting patterns within Manhattan.
    """)

# ============================================================================
# TAB 4: TIPS ANALYSIS (LINE CHART)
# ============================================================================
with tab4:
    st.subheader("4. Total Tips Revenue Over Time")
    
    daily_tips = filtered_df.groupby('pickup_date')['total_tips'].sum().reset_index()
    daily_tips['date'] = pd.to_datetime(daily_tips['pickup_date'])
    
    fig_tips = px.line(
        daily_tips,
        x='date',
        y='total_tips',
        markers=True,
        title='Daily Tips Revenue',
        labels={'date': 'Date', 'total_tips': 'Total Tips ($)'},
        line_shape='spline'
    )
    fig_tips.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig_tips, use_container_width=True)
    
    st.markdown("""
    **Insights:**
    - Tips revenue correlates strongly with overall trip volume, showing similar temporal patterns.
    - High-volume days generate significantly more tips in absolute terms.
    - The consistency of tipping behavior indicates a stable customer base with predictable gratuity patterns.
    """)

# ============================================================================
# TAB 5: PASSENGER PATTERNS (HEATMAP)
# ============================================================================
with tab5:
    st.subheader("5. Trip Volume Heatmap: Day of Week vs Hour")
    
    # Create pivot table for heatmap
    heatmap_data = filtered_df.pivot_table(
        index='hour',
        columns='day_of_week',
        values='num_trips',
        aggfunc='mean'
    )
    
    # Reorder columns by day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data[[col for col in day_order if col in heatmap_data.columns]]
    
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Day of Week", y="Hour of Day", color="Avg Trips"),
        title='Trip Volume Heatmap (Day of Week vs Hour)',
        color_continuous_scale='YlOrRd',
        aspect='auto'
    )
    fig_heatmap.update_layout(height=600)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("""
    **Insights:**
    - Clear weekly patterns emerge with weekday rush hours (7-9 AM, 5-7 PM) showing elevated trip volumes.
    - Weekend patterns differ from weekdays, with more distributed demand throughout the day.
    - Late night hours (midnight-4 AM) consistently show lower volumes across all days, except potential weekend entertainment peaks.
    """)

st.divider()

# ============================================================================
# DATA TABLE
# ============================================================================
st.header("📋 Data Preview")

if st.checkbox("Show filtered data table"):
    st.dataframe(
        filtered_df[['date', 'hour', 'num_trips', 'total_distance', 'total_fares', 'total_tips', 'avg_fare', 'avg_distance']].head(100),
        use_container_width=True,
        height=400
    )

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
---
**Dashboard Information:**
- Data Source: NYC Yellow Taxi Trip Records (January 2024)
- Data Granularity: Hourly aggregated statistics
- Last Updated: February 2026
- All visualizations are interactive — hover for details, click legend items to toggle series
""")
