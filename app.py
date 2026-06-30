import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration to wide layout and professional title
st.set_page_config(page_title="AI Customer Segmentation Dashboard", layout="wide")

# App Header Title
st.title(" E-Commerce AI Customer Segmentation Dashboard")
st.markdown("Powered by K-Means Clustering & RFM Analysis | Developed by Priti")
st.markdown("---")

# Load the final segmented  dataset
@st.cache_data
def load_data():
    df = pd.read_csv('online_retail_segmented.csv')
    return df
try:
    rfm = load_data()  
    # ------------
    # TOP ROW: HIGH LEVEL KPI METRICS
    # ------------
    total_customers = rfm.shape[0]
    avg_recency = round(rfm['Recency'].mean(), 1)
    avg_frequency = round(rfm['Frequency'].mean(), 1)
    total_revenue = f"£{rfm['Monetary'].sum():,.2f}"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Segmented Customers",value=total_customers)
    with col2:
        st.metric(label="Average Recency", value=f"{avg_recency} Days")
    with col3:
        st.metric(label="Average Orders / Customers", value=avg_frequency)
    with col4:
        st.metric(label="Total Database Value", value=total_revenue)

    st.markdown("---")   

    # ------
    # MAIN CONTENT SECTION: TWO SIDE-BY-SIDE PANELS
    # ---------
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.header(" Individual Customer Lookup") 
        customer_id = st.number_input("Enter a valid Customer ID:", min_value=int(rfm['CustomerID'].min()),max_value=int(rfm['CustomerID'].max()), step=1)

        if customer_id in rfm['CustomerID'].values:
            cust_data = rfm[rfm['CustomerID'] == customer_id].iloc[0]
            st.success(f"### **Assigned Cluster: {int(cust_data['Cluster'])}**")

            # Show individual metrics
            st.write(f" ** Recency:** {int(cust_data['Recency'])} days ago")
            st.write(f" **Frequency:** {int(cust_data['Frequency'])} total orders")
            st.write(f" **Monetary Spend:** £{cust_data['Monetary']:,.2f}")
        else:
            st.warning("Customer ID not found in current logs.")
    with right_col:
        st.header("Explore Segment Cluster Averages")   

        # Aggregate cluster profiles live
        cluster_profiles = rfm.groupby('Cluster').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'CustomerID': 'count'
        }).rename(columns={'CustomerID': 'Total Customers'}).round(2)

        st.dataframe(cluster_profiles, use_container_width=True)

        # Let the user download the segmented CSV directlyfrom the web interface
        st.markdown("### Download Segmented Output Data")
        csv = rfm.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Master online_retail_segmented.csv",
            data=csv,
            file_name='online_retail_segmented.csv',
           mime='text/csv',
        )
except FileNotFoundError:      
    st.error("X 'online_retail_segmented.csv' not found. please ensure you have successfully completed Day 4 Day 5 scripts first!")


# ------------
# NEW SECTION: ADD VISUALIZATIONS TO THE WEB APP
# ---------------
st.markdown("---")   
st.header("Model Visualisation & Analytics") 

# Create tabs to neatly switch between different graph
tab1, tab2 =st.tabs(["Customer Snake Plot", " Elbow Curve Optimization"])

with tab1:
    st.subheader("Customer Behaviour Profiles (Snake Plot)")
    try:
        st.image("rfm_snake_plot.png", use_container_width=True)
        st.caption("This chart maps how each unique cluster peaks or valleys across standardized Recency, Frequency, and Monetary scores.")
    except FileNotFoundError:
        st.warning(" 'rfm_snake_plot.png' chart not found in your directory. Run Day 5 script to generateir!")
with tab2:
    st.subheader("K-Means Elbow Optimization Curve")   

try:
        st.image("rfm_elbow_curve.png", use_container_width=True) 
        st.caption("The mathematical 'elbow point' shows the exact inflection boundaryjustifying why K=4 is the ideal number of customer segments.")
except FileNotFoundError:        
        st.warning("rfm_elbow_curve.png' chart not found in your directory.Run Day 4 script to generate it!")    

