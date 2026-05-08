import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Industry 4.0 Dashboard",
    layout="wide"
)

st.title("Manufacturing Industry 4.0 Dashboard")
st.markdown("### Streamlit Visualization Dashboard")

df = pd.read_csv("ai4i2020.csv")

df.columns = df.columns.str.strip()

st.sidebar.header("Filter Data")

machine_type = st.sidebar.multiselect(
    "Select Machine Type",
    options=df["Type"].unique(),
    default=df["Type"].unique()
)

filtered_df = df[df["Type"].isin(machine_type)]

total_machines = len(filtered_df)
failures = filtered_df["Machine failure"].sum()
failure_rate = round((failures / total_machines) * 100, 2)

avg_air_temp = round(filtered_df["Air temperature [K]"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Machines", total_machines)

with col2:
    st.metric("Machine Failures", failures)

with col3:
    st.metric("Failure Rate", f"{failure_rate}%")

with col4:
    st.metric("Average Air Temp", avg_air_temp)

st.divider()

st.subheader("Machine Failure Distribution")

fig_pie = px.pie(
    filtered_df,
    names="Machine failure",
    title="Failure vs Non-Failure"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Air Temperature Trend")

fig_temp = px.line(
    filtered_df.head(200),
    y="Air temperature [K]",
    title="Air Temperature Analysis"
)

st.plotly_chart(fig_temp, use_container_width=True)

st.subheader("RPM vs Torque Analysis")

fig_scatter = px.scatter(
    filtered_df,
    x="Rotational speed [rpm]",
    y="Torque [Nm]",
    color="Machine failure",
    title="Machine Performance Analysis"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Tool Wear Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Tool wear [min]",
    color="Machine failure",
    title="Tool Wear Analysis"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Machine Type Failure Analysis")

machine_failure = (
    filtered_df.groupby("Type")["Machine failure"]
    .sum()
    .reset_index()
)

fig_bar = px.bar(
    machine_failure,
    x="Type",
    y="Machine failure",
    title="Failures by Machine Type"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Correlation Heatmap")

corr = filtered_df.select_dtypes(include="number").corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.subheader("Sensor Monitoring Dashboard")

sensor_data = filtered_df[[
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]"
]].head(100)

st.line_chart(sensor_data)

st.subheader("Machine Health Gauge")

healthy_machines = filtered_df[
    filtered_df["Machine failure"] == 0
].shape[0]

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=healthy_machines,
    title={"text": "Healthy Machines"},
    gauge={
        "axis": {"range": [0, total_machines]}
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

st.subheader("Raw Dataset")

st.dataframe(filtered_df)

st.markdown("---")
st.markdown("Industry 4.0 Manufacturing Dashboard using Streamlit")