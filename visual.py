import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Industry 4.0 Dashboard",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
    Manufacturing Industry 4.0 Dashboard
    </h1>

    <h4 style='text-align: center; color: gray;'>
    Real-Time Manufacturing Analytics & Visualization
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

df = pd.read_csv("ai4i2020.csv")

df.columns = df.columns.str.strip()

st.sidebar.header("Dashboard Filters")

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
avg_rpm = round(filtered_df["Rotational speed [rpm]"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Machines", total_machines)

with col2:
    st.metric("Machine Failures", failures)

with col3:
    st.metric("Failure Rate", f"{failure_rate}%")

with col4:
    st.metric("Average RPM", avg_rpm)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    fig_pie = px.pie(
        filtered_df,
        names="Machine failure",
        hole=0.5,
        title="Failure Distribution"
    )

    fig_pie.update_layout(
        title_x=0.3,
        height=500
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with col2:

    fig_bar = px.bar(
        filtered_df.groupby("Type")["Machine failure"]
        .sum()
        .reset_index(),
        x="Type",
        y="Machine failure",
        title="Machine Type Failure Analysis",
        text_auto=True
    )

    fig_bar.update_layout(
        title_x=0.25,
        height=500
    )

    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

fig_temp = px.line(
    filtered_df,
    x=filtered_df.index,
    y=[
        "Air temperature [K]",
        "Process temperature [K]"
    ],
    title="Temperature Monitoring Analysis"
)

fig_temp.update_layout(
    title_x=0.35,
    height=600
)

st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

fig_scatter = px.scatter(
    filtered_df,
    x="Rotational speed [rpm]",
    y="Torque [Nm]",
    color="Machine failure",
    size="Tool wear [min]",
    hover_data=[
        "Air temperature [K]",
        "Process temperature [K]"
    ],
    title="RPM vs Torque Performance Analysis"
)

fig_scatter.update_layout(
    title_x=0.3,
    height=700
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

corr = filtered_df.select_dtypes(include="number").corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

fig_heatmap.update_layout(
    title_x=0.38,
    height=700
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

sensor_data = filtered_df[[
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]"
]]

st.subheader("Real-Time Sensor Monitoring")

st.line_chart(sensor_data)

st.markdown("---")

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

fig_gauge.update_layout(
    height=500
)

st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

st.subheader("Manufacturing Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.markdown(
    """
    <h5 style='text-align: center; color: gray;'>
    Industry 4.0 Manufacturing Analytics Dashboard using Streamlit
    </h5>
    """,
    unsafe_allow_html=True
)