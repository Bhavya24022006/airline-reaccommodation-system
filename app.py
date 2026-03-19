import streamlit as st
import pandas as pd

 

@st.cache_data
def load_data():
    assignments = pd.read_csv("data/processed/final_assignments_advanced.csv")
    return assignments

df = load_data()

 

st.title("Airline Passenger Re-accommodation System")

 

total = len(df)
multi = len(df[df['type'] == 'multi_hop'])
direct = len(df[df['type'] == 'direct'])

st.subheader("System Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Assigned", total)
col2.metric("Direct", direct)
col3.metric("Multi-hop", multi)

 

st.subheader("Search Passenger")

pnr_input = st.text_input("Enter PNR ID")

if pnr_input:
    result = df[df['pnr_id'] == pnr_input]

    if not result.empty:
        row = result.iloc[0]

        st.success("Passenger Found")

        st.write("PNR ID:", row['pnr_id'])
        st.write("Passenger ID:", row['passenger_id'])
        st.write("Old Flight:", row['old_flight'])
        st.write("New Flight:", row['new_flight'])
        st.write("Type:", row['type'])
        st.write("Reason:", row['reason'])

    else:
        st.error("Passenger not found")
 

st.subheader("All Assignments")

st.dataframe(df)