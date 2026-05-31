import streamlit as st
import pandas as pd
import json
import subprocess
import datetime

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Horizon Airways Operations Terminal")

# ==========================================
# CUSTOM AIRPORT BRANDING & CSS INJECTION
# ==========================================
st.markdown("""
    <style>
        /* Main page adjustments */
        .main {
            background-color: #0A192F;
            color: #F4F6F9;
        }
        
        /* Typography overrides */
        h1 {
            color: #FFFFFF !important;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
            border-bottom: 2px solid #1E3A8A;
            padding-bottom: 10px;
        }
        h2, h3 {
            color: #64748B !important;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-weight: 600 !important;
        }
        
        /* Metric Card Container Layouts */
        div[data-testid="stMetric"] {
            background-color: #112240 !important;
            border: 1px solid #233554 !important;
            border-radius: 6px !important;
            padding: 15px 20px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        div[data-testid="stMetricLabel"] > div {
            color: #8892B0 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        div[data-testid="stMetricValue"] > div {
            color: #64FFDA !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        /* Custom Airline Banner Info Bar */
        .airport-banner {
            background: linear-gradient(90deg, #1E3A8A 0%, #0F172A 100%);
            border-left: 5px solid #F59E0B;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 25px;
            color: #E2E8F0;
        }
        
        /* Tab formatting */
        button[data-baseweb="tab"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #8892B0 !important;
        }
        button[aria-selected="true"] {
            color: #64FFDA !important;
            border-bottom-color: #64FFDA !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR: BUSINESS RULE ENGINE TERMINAL
# ==========================================
st.sidebar.markdown("### Operations Control Panel")
st.sidebar.title("Business Rule Engine")

# Load existing configuration rules
with open("rules_config.json", "r") as f:
    config = json.load(f)

st.sidebar.markdown("---")
st.sidebar.subheader("Passenger Priority Weights")
u_minor_score = st.sidebar.slider("Unaccompanied Minor Parameters", 10, 100, int(config["passenger_priorities"]["UNACCOMPANIED_MINOR_SCORE"]))
emp_score = st.sidebar.slider("On-Duty Crew Assignment Weight", 10, 100, int(config["passenger_priorities"]["ON_DUTY_EMPLOYEE_SCORE"]))

st.sidebar.markdown("---")
st.sidebar.subheader("Routing Strategy Restraints")
allow_multihop_minors = st.sidebar.checkbox("Allow Interline Connecting Paths for Minors", value=config["constraints"]["ALLOW_MULTIHOP_FOR_MINORS"])

# TTL Slider configuration
solution_ttl_hours = st.sidebar.slider("Operational Batch Expiration Window (Hours)", 1, 48, 6)

st.sidebar.markdown("---")
# Save and trigger recalculation sequence
if st.sidebar.button("Apply Parameters & Re-route Fleet"):
    # Update config memory mapping structure
    config["passenger_priorities"]["UNACCOMPANIED_MINOR_SCORE"] = u_minor_score
    config["passenger_priorities"]["ON_DUTY_EMPLOYEE_SCORE"] = emp_score
    config["constraints"]["ALLOW_MULTIHOP_FOR_MINORS"] = allow_multihop_minors
    
    # Save configurations back out to root JSON
    with open("rules_config.json", "w") as f:
        json.dump(config, f, indent=2)
        
    st.sidebar.info("Processing fleet optimization updates...")
    
    # Calculate and store the expiration timestamp when the button is pushed
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=solution_ttl_hours)
    st.session_state["solution_expires_at"] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Fire off core reaccommodation loop
    subprocess.run(["python", "reaccommodation.py"])
    
    # Clear cache to force Streamlit to read new data files
    st.cache_data.clear()
    st.sidebar.success("Optimization Manifest Updated.")

# ==========================================
# MAIN DASHBOARD OPERATIONAL HEADER
# ==========================================
st.title("Horizon Airways Flight Operations Center")

# Airport Banner Display
if "solution_expires_at" in st.session_state:
    st.markdown(f"""
        <div class="airport-banner">
            <strong>System Operational Status:</strong> Optimization manifest locked. 
            Batch solution validity window scheduled to expire at: <code>{st.session_state['solution_expires_at']}</code>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="airport-banner">
            <strong>System Operational Status:</strong> Production database online. 
            Adjust rule configurations to initialize network routing metrics.
        </div>
    """, unsafe_allow_html=True)

# Helper loaders for updated runs (Cached until rules are reset)
@st.cache_data
def load_processed_data():
    try:
        df_assigned = pd.read_csv("data/processed/final_assignments_advanced.csv")
        df_exceptions = pd.read_csv("data/processed/exceptions_advanced.csv")
    except:
        df_assigned = pd.DataFrame()
        df_exceptions = pd.DataFrame()
    return df_assigned, df_exceptions

df_assigned, df_exceptions = load_processed_data()

total_assigned = len(df_assigned)
total_exceptions = len(df_exceptions)
total_impacted = total_assigned + total_exceptions

# High Level Performance KPIs
st.subheader("Network Routing Analysis")
col1, col2, col3, col4, col5 = st.columns(5)

if total_impacted > 0:
    success_rate = round((total_assigned / total_impacted) * 100, 2)
    direct_count = len(df_assigned[df_assigned['type'] == 'direct'])
    multi_count = len(df_assigned[df_assigned['type'] == 'multi_hop'])
else:
    success_rate = 0.0
    direct_count, multi_count = 0, 0

col1.metric("Total Disrupted Records", total_impacted)
col2.metric("Accommodated Passengers", total_assigned)
col3.metric("Direct Routings Assigned", direct_count)
col4.metric("Multi-Hop Connection Paths", multi_count)
col5.metric("System Accomplishment Index", f"{success_rate}%")

# Distinct Exception Metric Block
st.markdown("<br>", unsafe_allow_html=True)
col_ex1 = st.columns(1)[0]
col_ex1.metric("Unresolved Exception Discrepancies (Requires Manual Desking)", total_exceptions)

# ==========================================
# AIRPORT INFORMATION CONTROL TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["Flight Assignment Log", "Unresolved Exceptions", "Passenger Check-In Query"])

with tab1:
    st.subheader("Confirmed Fleet Level Manifests")
    if not df_assigned.empty:
        st.dataframe(df_assigned, use_container_width=True)
    else:
        st.info("No active re-accommodation data arrays stored in this sector.")

with tab2:
    st.subheader("Isolated PNR Level Exceptions")
    if not df_exceptions.empty:
        st.dataframe(df_exceptions, use_container_width=True)
    else:
        st.success("Manifest clean. Zero unassigned records tracking within the database.")

with tab3:
    st.subheader("Passenger Security & Itinerary Resolution")
    pnr_input = st.text_input("Scan Passenger PNR Record Number:")
    if pnr_input:
        match_assigned = df_assigned[df_assigned['pnr_id'] == pnr_input] if not df_assigned.empty else pd.DataFrame()
        match_exception = df_exceptions[df_exceptions['pnr_id'] == pnr_input] if not df_exceptions.empty else pd.DataFrame()
        
        if not match_assigned.empty:
            row = match_assigned.iloc[0]
            st.success("Passenger itinerary successfully re-routed and validated.")
            
            # Formatted key-value metric printout representing boarding pass info
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Booking Reference (PNR ID):** `{row['pnr_id']}`")
            c1.markdown(f"**Customer Identification:** {row['passenger_id']}")
            c2.markdown(f"**Disrupted Sector Leg:** {row['old_flight']}")
            c2.markdown(f"**Re-routed Accommodation Leg:** `{row['new_flight']}`")
            c3.markdown(f"**Routing Classification:** {str(row['type']).upper()}")
            c3.markdown(f"**Resolution Allocation Details:** {row['reason']}")
            
        elif not match_exception.empty:
            st.error("Itinerary Blocked. Passenger status flags active inside Exception Roster.")
            st.dataframe(match_exception)
        else:
            st.warning("PNR reference out of bounds. Record tracking sequence not found in active operational data.")