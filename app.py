import streamlit as st
import pandas as pd
st.set_page_config(
 page_title='NYC Taxi Dashboard',
 page_icon='taxi',
 layout='wide'
)
st.title('NYC Taxi Trip Dashboard')
@st.cache_data
def load_data():
 df = pd.read_parquet('../data/raw/taxi_data.parquet')
 return df.sample(n=100000, random_state=42)
df = load_data()
# Display key metrics
col1, col2, col3 = st.columns(3)
col1.metric('Total Trips', f'{len(df):,}')
col2.metric('Avg Fare', f'${df["fare_amount"].mean():.2f}')
col3.metric('Avg Distance', f'{df["trip_distance"].mean():.2f} mi')
st.sidebar.success('Select a page above.')

st.sidebar.header('Filters')
fare_range = st.sidebar.slider(
 'Fare Range ($)',
 min_value=0.0,
 max_value=100.0,
 value=(0.0, 50.0)
)
# Apply filter
filtered_df = df[
 (df['fare_amount'] >= fare_range[0]) &
 (df['fare_amount'] <= fare_range[1])
]

import altair as alt

brush = alt.selection_interval()
scatter = alt.Chart(df).mark_circle().encode(
 x='trip_distance:Q',
 y='fare_amount:Q',
 color=alt.condition(brush, 'pickup_hour:O', alt.value('lightgray'))
).add_params(brush)
histogram = alt.Chart(df).mark_bar().encode(
 x='pickup_hour:O',
 y='count()',
 color=alt.condition(brush, alt.value('steelblue'), alt.value('lightgray'))
).add_params(brush)
st.altair_chart(scatter | histogram)



uploaded = st.file_uploader('Choose a CSV', type='csv')
if uploaded is not None:
 df = pd.read_csv(uploaded)
 st.dataframe(df.head(20))
 # Let user select columns for visualization
 x_col = st.selectbox('X-axis', df.columns)
 y_col = st.selectbox('Y-axis', df.columns)
 fig = px.scatter(df, x=x_col, y=y_col)
 st.plotly_chart(fig)