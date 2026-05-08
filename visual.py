import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Credit Card Customer Analytics Dashboard",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center; color:#0E76A8;'>
    Credit Card Customer Analytics Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("credit_card.csv")

df.columns = df.columns.str.strip()

st.sidebar.title("Dashboard Controls")

rows = st.sidebar.slider(
    "Select Number of Rows",
    min_value=100,
    max_value=len(df),
    value=3000
)

selected_chart = st.sidebar.selectbox(
    "Select Main Chart",
    [
        "Balance vs Purchases",
        "Purchases vs Payments",
        "Credit Limit Analysis",
        "Cash Advance Analysis",
        "Minimum Payments",
        "Customer Tenure",
        "Installment Purchases",
        "Payments vs Credit Limit"
    ]
)

theme = st.sidebar.radio(
    "Select Theme",
    ["Light", "Dark"]
)

show_data = st.sidebar.checkbox(
    "Show Raw Dataset"
)

show_statistics = st.sidebar.checkbox(
    "Show Summary Statistics",
    value=True
)

filtered_df = df.head(rows)

st.divider()

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
        "Average Balance",
        round(
            filtered_df["BALANCE"].mean(),
            2
        )
    )

with col3:

    st.metric(
        "Average Purchases",
        round(
            filtered_df["PURCHASES"].mean(),
            2
        )
    )

with col4:

    st.metric(
        "Average Credit Limit",
        round(
            filtered_df["CREDIT_LIMIT"].mean(),
            2
        )
    )

col5, col6 = st.columns(2)

with col5:

    st.metric(
        "Average Payments",
        round(
            filtered_df["PAYMENTS"].mean(),
            2
        )
    )

with col6:

    st.metric(
        "Average Cash Advance",
        round(
            filtered_df["CASH_ADVANCE"].mean(),
            2
        )
    )

st.divider()

if selected_chart == "Balance vs Purchases":

    st.subheader(
        "1. Balance vs Purchases"
    )

    fig1 = px.scatter(
        filtered_df,
        x="BALANCE",
        y="PURCHASES",
        color="TENURE",
        title="Balance vs Purchases"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

elif selected_chart == "Purchases vs Payments":

    st.subheader(
        "2. Purchases vs Payments"
    )

    fig2 = px.scatter(
        filtered_df,
        x="PURCHASES",
        y="PAYMENTS",
        color="CREDIT_LIMIT",
        title="Purchases vs Payments"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

elif selected_chart == "Credit Limit Analysis":

    st.subheader(
        "3. Credit Limit Analysis"
    )

    fig3 = px.box(
        filtered_df,
        y="CREDIT_LIMIT",
        color="TENURE",
        title="Credit Limit Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

elif selected_chart == "Cash Advance Analysis":

    st.subheader(
        "4. Cash Advance vs Balance"
    )

    fig4 = px.scatter(
        filtered_df,
        x="CASH_ADVANCE",
        y="BALANCE",
        color="PAYMENTS",
        title="Cash Advance vs Balance"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

elif selected_chart == "Minimum Payments":

    st.subheader(
        "5. Minimum Payments by Customer"
    )

    fig5 = px.bar(
        filtered_df.head(20),
        x="CUST_ID",
        y="MINIMUM_PAYMENTS",
        color="MINIMUM_PAYMENTS",
        title="Minimum Payments Analysis"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

elif selected_chart == "Customer Tenure":

    st.subheader(
        "6. Customer Tenure Analysis"
    )

    tenure_df = filtered_df.groupby(
        "TENURE"
    )["BALANCE"].mean().reset_index()

    fig6 = px.line(
        tenure_df,
        x="TENURE",
        y="BALANCE",
        markers=True,
        title="Average Balance by Customer Tenure"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

elif selected_chart == "Installment Purchases":

    st.subheader(
        "7. Installment Purchases Analysis"
    )

    fig7 = px.scatter(
        filtered_df,
        x="INSTALLMENTS_PURCHASES",
        y="PURCHASES",
        color="BALANCE",
        title="Installment Purchases vs Total Purchases"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

else:

    st.subheader(
        "8. Payments vs Credit Limit"
    )

    fig8 = px.scatter(
        filtered_df,
        x="PAYMENTS",
        y="CREDIT_LIMIT",
        color="BALANCE",
        title="Payments vs Credit Limit"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )