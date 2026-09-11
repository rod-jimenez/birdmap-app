import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="State Unique Values Dashboard",
    layout="wide"
)

st.title("🇺🇸 State Unique Values Dashboard")
st.subheader("Visualizing the count of unique values per state using an interactive map")


# 2. Import Data
df = pd.read_csv("D:/Users/Rod/Desktop/ebird_US-concat__1900_2025_1_12_barchart.txt", sep="\t")


# 3. Sidebar Configuration for Customization
st.sidebar.header("Map Configurations")
color_theme = st.sidebar.selectbox(
    "Select Color Scale Theme",
    options=["Viridis", "Cividis", "Blues", "Reds", "Greens", "Plasma"],
    index=0
)

# 4. Data Processing: Calculate Unique Values per State
# Grouping by state and finding the number of unique entries in 'category'
state_metrics = df.groupby("State")["Species"].nunique().reset_index()
state_metrics.columns = ["state", "unique_count"]

# 5. Displaying Metrics in Columns
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📊 Calculated Metrics")
    st.dataframe(
        state_metrics.sort_values(by="unique_count", ascending=False),
        column_config={
            "state": "State Abbreviation",
            "unique_count": st.column_config.NumberColumn(
                "Unique Values Count",
                format="%d 🔢"
            )
        },
        hide_index=True,
        use_container_width=True
    )

with col1:
    # 6. Build the Plotly Choropleth Map
    fig = px.choropleth(
        state_metrics,
        locations="state",           # Column containing state codes (e.g. CA, NY)
        locationmode="USA-states",   # Tell Plotly to identify US State layouts
        color="unique_count",        # The column mapping to the color scale
        color_continuous_scale=color_theme,
        scope="usa",                 # Constrain map view to USA
        labels={"unique_count": "Unique Items"},
        title="Unique Value Counts by US State"
    )
    
    # Update layout padding to make the map look seamless
    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    
    # Render the chart inside Streamlit
    st.plotly_chart(fig, use_container_width=True)