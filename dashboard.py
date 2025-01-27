import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Driver Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        .metric-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Mock data creation based on your analysis results
def create_mock_data():
    dates = pd.date_range(start='2012-09-10', end='2012-09-24', freq='H')
    
    # Create data using the actual datetime objects
    df = pd.DataFrame({
        'datetime': dates,
        'Completed Trips': [int(50 + i + (dates[i].hour/24)*100) for i in range(len(dates))],
        'Unique Drivers': [int(40 + (dates[i].hour/24)*50) for i in range(len(dates))],
        'Requests': [int(60 + (dates[i].hour/24)*80) for i in range(len(dates))],
        'Zeroes': [int(10 + (dates[i].hour/24)*20) for i in range(len(dates))],
        'Eyeballs': [int(30 + (dates[i].hour/24)*40) for i in range(len(dates))]
    })
    
    # Add weekend pattern
    df['is_weekend'] = df['datetime'].dt.dayofweek.isin([4, 5, 6])
    df.loc[df['is_weekend'], ['Completed Trips', 'Requests']] *= 1.5
    
    return df

def main():
    st.title("🚗 Driver Analytics Dashboard")
    
    # Load data
    df = create_mock_data()
    
    # Key Metrics Section
    st.markdown("### 📊 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-container">
                <div class="metric-value">278</div>
                <div class="metric-label">Highest Trips (24h)</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="metric-container">
                <div class="metric-value">44.86%</div>
                <div class="metric-label">Weekend Zeroes</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="metric-container">
                <div class="metric-value">0.51</div>
                <div class="metric-label">Trips per Driver</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class="metric-container">
                <div class="metric-value">4:00</div>
                <div class="metric-label">Optimal End Time</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### 📈 Performance Analysis")
    
    # Row 1 - Time Series
    col1, col2 = st.columns(2)
    
    with col1:
        # Trips Over Time
        fig_trips = px.line(df, x='datetime', y='Completed Trips',
                           title='Completed Trips Over Time')
        fig_trips.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Number of Trips"
        )
        st.plotly_chart(fig_trips, use_container_width=True)
    
    with col2:
        # Supply vs Demand
        fig_supply = px.line(df, x='datetime', y=['Unique Drivers', 'Requests'],
                            title='Supply vs Demand Analysis')
        fig_supply.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Count",
            legend_title="Metric"
        )
        st.plotly_chart(fig_supply, use_container_width=True)
    
    # Row 2 - Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly patterns
        hourly_data = df.groupby(df['datetime'].dt.hour)['Requests'].mean().reset_index()
        fig_hourly = px.bar(hourly_data, x='datetime', y='Requests',
                           title='Average Hourly Request Pattern')
        fig_hourly.update_layout(
            height=400,
            xaxis_title="Hour of Day",
            yaxis_title="Average Requests"
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        # Zeroes vs Eyeballs correlation
        fig_correlation = px.scatter(df, x='Eyeballs', y='Zeroes',
                                   color='Completed Trips',
                                   title='Eyeballs vs Zeroes Distribution')
        fig_correlation.update_layout(
            height=400,
            xaxis_title="Eyeballs",
            yaxis_title="Zeroes"
        )
        st.plotly_chart(fig_correlation, use_container_width=True)
    
    # Additional Insights Section
    st.markdown("### 🎯 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        📌 **Peak Performance**
        - Busiest 8-hour shift starts at 16:00
        - Maximum 192 unique requests during peak
        - Optimal driver allocation during evening hours
        """)
    
    with col2:
        st.info("""
        📌 **Supply-Demand Patterns**
        - Weekend zeroes constitute 44.86% of total zeroes
        - Supply-demand mismatch highest during late nights
        - Early morning (4:00) identified as optimal end time
        """)

if __name__ == "__main__":
    main()