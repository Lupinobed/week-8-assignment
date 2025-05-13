import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime

# App config
st.set_page_config(page_title="Data Insights Dashboard", layout="wide")
st.title("📊 Insights & Reporting Dashboard")

# Sample data generation (replace with your actual data)
@st.cache_data
def load_data():
    # Vaccination data
    countries = ['Country X', 'Country Y', 'Country Z', 'Country A', 'Country B']
    vaccination_rates = [70, 45, 38, 52, 28]
    
    # Engagement data
    dates = pd.date_range(start="2023-01-01", end="2023-12-31")
    engagement = np.random.normal(100, 10, len(dates))
    engagement[120:] *= 0.7  # 30% drop after policy change
    
    # Revenue data
    weekdays = [d.strftime('%A') for d in dates]
    revenue = np.where(np.array(weekdays).isin(['Saturday', 'Sunday']), 
                      np.random.normal(125, 5, len(dates)), 
                      np.random.normal(100, 5, len(dates)))
    
    # Demographic data
    age_groups = ['18-24', '25-34', '35-44', '45+']
    old_dist = [15, 40, 30, 15]
    new_dist = [40, 35, 15, 10]
    
    # Complaints data
    regions = ['Region A', 'Region B', 'Region C']
    complaints = {
        'Q1': [20, 15, 10],
        'Q2': [25, 18, 12],
        'Q3': [60, 20, 15],  # 200% increase in Region A
        'Q4': [30, 22, 18]
    }
    
    return {
        'vaccination': pd.DataFrame({'Country': countries, 'Rate': vaccination_rates}),
        'engagement': pd.DataFrame({'Date': dates, 'Engagement': engagement}),
        'revenue': pd.DataFrame({'Date': dates, 'Revenue': revenue, 'Day': weekdays}),
        'demographics': pd.DataFrame({'Age Group': age_groups, 'Old': old_dist, 'New': new_dist}),
        'complaints': pd.DataFrame(complaints, index=regions).reset_index().melt(id_vars='index', var_name='Quarter', value_name='Complaints')
    }

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Country", data['vaccination']['Country'])

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Vaccination", "Engagement", "Revenue", "Demographics"])

with tab1:
    st.header("1. Country X Had the Fastest Vaccine Rollout")
    fig = px.bar(data['vaccination'], x='Country', y='Rate', 
                 title="Vaccination Rates by Country", color='Rate')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    *Key Insight*:  
    - Country X vaccinated *70% of its population* within 3 months  
    - Likely due to strong government policies + high public trust  
    """)

with tab2:
    st.header("2. Unexpected Drop in Engagement After Policy Change")
    policy_date = datetime(2023, 5, 1)
    fig = px.line(data['engagement'], x='Date', y='Engagement', 
                 title="User Engagement Over Time")
    fig.add_vline(x=policy_date, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    *Anomaly*:  
    - 30% drop observed after Policy Y introduction (May 2023)  
    - Possible cause: Stricter data privacy rules reduced tracking  
    """)

with tab3:
    st.header("3. Revenue Peaks on Weekends")
    fig = px.box(data['revenue'], x='Day', y='Revenue', 
                title="Revenue Distribution by Day of Week",
                category_orders={'Day': ['Monday', 'Tuesday', 'Wednesday', 
                                       'Thursday', 'Friday', 'Saturday', 'Sunday']})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    *Pattern*:  
    - Saturdays show *25% higher revenue* than weekdays  
    - Recommendation: Increase ad spend on Fridays/weekends  
    """)

with tab4:
    st.header("4. Demographic Shift in Product Users")
    fig = px.pie(data['demographics'], values='New', names='Age Group', 
                title="Current Age Distribution of Users")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    *Trend*:  
    - Users aged 18-24 grew from 15% to 40% in 6 months  
    - Marketing should pivot to younger audiences  
    """)

# Complaints section
st.header("5. Anomaly: Spikes in Customer Complaints")
fig = px.bar(data['complaints'], x='Quarter', y='Complaints', color='index',
             title="Customer Complaints by Region", barmode='group')
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
*Key Finding*:  
- Region A saw *200% increase* in complaints during Q3 2023  
- Root cause: Supply chain delays led to late deliveries  
""")

# Additional insights
with st.expander("Bonus Insights"):
    st.write("""
    - *Seasonality*: Demand drops 15% every January  
    - *VIP Customer*: One user accounted for 5% of total revenue  
    - *Correlation*: Website traffic → +12% conversion rate (r = 0.89)  
    """)