import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center; color:#0E76A8;'>
    Bank Customer Churn Analytics Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("BankChurners.csv")

df.columns = df.columns.str.strip()

st.sidebar.title("Dashboard Controls")

rows = st.sidebar.slider(
    "Select Number of Rows",
    min_value=100,
    max_value=len(df),
    value=3000
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

selected_card = st.sidebar.selectbox(
    "Select Card Category",
    df["Card_Category"].unique()
)

analysis_type = st.sidebar.selectbox(
    "Select Financial Analysis",
    [
        "Customer Age Analysis",
        "Credit Limit Analysis",
        "Transaction Analysis",
        "Income Analysis",
        "Gender Analysis",
        "Card Category Analysis",
        "Utilization Analysis",
        "Customer Relationship Analysis"
    ]
)

show_statistics = st.sidebar.checkbox(
    "Show Summary Statistics",
    value=True
)

show_kpi = st.sidebar.checkbox(
    "Show KPI Metrics",
    value=True
)

show_data = st.sidebar.checkbox(
    "Show Raw Dataset"
)

credit_limit_range = st.sidebar.slider(
    "Credit Limit Range",
    int(df["Credit_Limit"].min()),
    int(df["Credit_Limit"].max()),
    (
        int(df["Credit_Limit"].min()),
        int(df["Credit_Limit"].max())
    )
)

filtered_df = df[
    (df["Gender"].isin(selected_gender)) &
    (df["Card_Category"] == selected_card) &
    (df["Credit_Limit"] >= credit_limit_range[0]) &
    (df["Credit_Limit"] <= credit_limit_range[1])
].head(rows)

st.divider()

if show_kpi:

    st.subheader(
        "Key Performance Indicators"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Customers",
            len(filtered_df)
        )

    with col2:

        st.metric(
            "Average Credit Limit",
            round(
                filtered_df["Credit_Limit"].mean(),
                2
            )
        )

    with col3:

        st.metric(
            "Average Transactions",
            round(
                filtered_df["Total_Trans_Amt"].mean(),
                2
            )
        )

    with col4:

        st.metric(
            "Average Utilization Ratio",
            round(
                filtered_df["Avg_Utilization_Ratio"].mean(),
                2
            )
        )

st.divider()

if analysis_type == "Customer Age Analysis":

    st.subheader(
        "1. Customer Age Analysis"
    )

    fig1 = px.histogram(
        filtered_df,
        x="Customer_Age",
        color="Attrition_Flag",
        title="Customer Age Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

elif analysis_type == "Credit Limit Analysis":

    st.subheader(
        "2. Credit Limit Analysis"
    )

    fig2 = px.box(
        filtered_df,
        y="Credit_Limit",
        color="Card_Category",
        title="Credit Limit Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

elif analysis_type == "Transaction Analysis":

    st.subheader(
        "3. Transaction Analysis"
    )

    fig3 = px.scatter(
        filtered_df,
        x="Total_Trans_Amt",
        y="Total_Trans_Ct",
        color="Attrition_Flag",
        title="Transactions Amount vs Count"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

elif analysis_type == "Income Analysis":

    st.subheader(
        "4. Income Analysis"
    )

    income_df = filtered_df.groupby(
        "Income_Category"
    )["Credit_Limit"].mean().reset_index()

    fig4 = px.bar(
        income_df,
        x="Income_Category",
        y="Credit_Limit",
        color="Income_Category",
        title="Average Credit Limit by Income"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

elif analysis_type == "Gender Analysis":

    st.subheader(
        "5. Gender Analysis"
    )

    fig5 = px.pie(
        filtered_df,
        names="Gender",
        title="Customer Gender Distribution"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

elif analysis_type == "Card Category Analysis":

    st.subheader(
        "6. Card Category Analysis"
    )

    card_df = filtered_df.groupby(
        "Card_Category"
    )["Total_Trans_Amt"].mean().reset_index()

    fig6 = px.line(
        card_df,
        x="Card_Category",
        y="Total_Trans_Amt",
        markers=True,
        title="Average Transaction Amount by Card Category"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

elif analysis_type == "Utilization Analysis":

    st.subheader(
        "7. Utilization Analysis"
    )

    fig7 = px.area(
        filtered_df.head(100),
        x="Customer_Age",
        y="Avg_Utilization_Ratio",
        title="Utilization Ratio by Age"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

else:

    st.subheader(
        "8. Customer Relationship Analysis"
    )

    fig8 = px.scatter(
        filtered_df,
        x="Total_Relationship_Count",
        y="Credit_Limit",
        color="Attrition_Flag",
        size="Total_Trans_Amt",
        title="Relationship Count vs Credit Limit"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

    st.subheader(
        "Summary Statistics"
    )

    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )

if show_data:

    st.divider()

    st.subheader(
        "Raw Dataset"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )