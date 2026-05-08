import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error


st.set_page_config(
    page_title="Industry 4.0 ML Dashboard",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center; color:#0E76A8;'>
    Industry 4.0 Machine Learning Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.divider()

df = pd.read_csv("cleaned_ai4i2020.csv")

df.columns = df.columns.str.strip()

machine_labels = {
    0: "Low",
    1: "Medium",
    2: "High"
}

df["Machine Type"] = df["Type"].map(machine_labels)

st.sidebar.title("Dashboard Controls")

selected_type = st.sidebar.multiselect(
    "Select Machine Type",
    options=df["Machine Type"].unique(),
    default=df["Machine Type"].unique()
)

selected_chart = st.sidebar.selectbox(
    "Select Main Chart",
    [
        "Process Temperature",
        "Torque vs RPM",
        "Machine Failure",
        "Tool Wear",
        "Torque Distribution"
    ]
)

show_data = st.sidebar.checkbox(
    "Show Raw Dataset"
)

show_metrics = st.sidebar.checkbox(
    "Show KPI Metrics",
    value=True
)

enable_prediction = st.sidebar.checkbox(
    "Enable Prediction",
    value=True
)

model_type = st.sidebar.radio(
    "Select Model",
    [
        "Linear Regression",
        "Logistic Regression"
    ]
)

rows = st.sidebar.slider(
    "Select Number of Rows",
    min_value=100,
    max_value=len(df),
    value=1000
)

air_temp = st.sidebar.slider(
    "Air Temperature",
    295,
    305,
    300
)

process_temp = st.sidebar.slider(
    "Process Temperature",
    305,
    315,
    310
)

rpm = st.sidebar.slider(
    "Rotational Speed",
    1000,
    3000,
    1500
)

torque = st.sidebar.slider(
    "Torque",
    0,
    100,
    40
)

tool_wear = st.sidebar.slider(
    "Tool Wear",
    0,
    300,
    100
)

filtered_df = df[
    df["Machine Type"].isin(selected_type)
].head(rows)

if show_metrics:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Machines",
            len(filtered_df)
        )

    with col2:
        st.metric(
            "Machine Failures",
            filtered_df["Machine failure"].sum()
        )

    with col3:
        st.metric(
            "Average RPM",
            round(
                filtered_df[
                    "Rotational speed [rpm]"
                ].mean(),
                2
            )
        )

    with col4:
        st.metric(
            "Average Torque",
            round(
                filtered_df[
                    "Torque [Nm]"
                ].mean(),
                2
            )
        )

st.divider()

st.subheader(
    "Process Temperature by Machine Type"
)

fig1 = px.bar(
    filtered_df,
    x="Machine Type",
    y="Process temperature [K]",
    color="Machine Type",
    title="Process Temperature by Machine Type"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()

st.subheader(
    "Torque vs Rotational Speed"
)

fig2 = px.scatter(
    filtered_df,
    x="Torque [Nm]",
    y="Rotational speed [rpm]",
    color="Machine failure",
    title="Torque vs Rotational Speed"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

st.subheader(
    "Machine Failure vs Air Temperature"
)

fig3 = px.pie(
    filtered_df,
    names="Machine failure",
    values="Air temperature [K]",
    hole=0.5,
    title="Machine Failure vs Air Temperature"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

st.subheader(
    "Tool Wear vs Machine Failure"
)

fig4 = px.box(
    filtered_df,
    x="Machine failure",
    y="Tool wear [min]",
    color="Machine failure",
    title="Tool Wear vs Machine Failure"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()

st.subheader(
    "Machine Failure by Machine Type"
)

fig5 = px.pie(
    filtered_df,
    names="Machine Type",
    hole=0.5,
    title="Machine Failure by Machine Type"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()

st.subheader(
    "Torque Distribution"
)

fig6 = px.box(
    filtered_df,
    y="Torque [Nm]",
    title="Torque Distribution"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.divider()

st.subheader(
    "Prediction Section"
)

if model_type == "Linear Regression":

    st.subheader(
        "Linear Regression"
    )

    X_linear = filtered_df[[
        "Air temperature [K]",
        "Process temperature [K]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]]

    y_linear = filtered_df[
        "Rotational speed [rpm]"
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X_linear,
        y_linear,
        test_size=0.2,
        random_state=42
    )

    linear_model = LinearRegression()

    linear_model.fit(
        X_train,
        y_train
    )

    linear_pred = linear_model.predict(
        X_test
    )

    fig6 = px.scatter(
        x=y_test,
        y=linear_pred,
        labels={
            "x": "Actual RPM",
            "y": "Predicted RPM"
        },
        title="Actual vs Predicted RPM"
    )

    fig6.update_layout(
        xaxis_title="Actual RPM",
        yaxis_title="Predicted RPM"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    r2 = r2_score(
        y_test,
        linear_pred
    )

    mse = mean_squared_error(
        y_test,
        linear_pred
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "R² Score",
            round(r2, 2)
        )

    with col2:

        st.metric(
            "Mean Squared Error",
            round(mse, 2)
        )


    st.write(
        "### Linear Regression Coefficients"
    )

    coefficient_df = pd.DataFrame({
        "Feature": X_linear.columns,
        "Coefficient": linear_model.coef_
    })

    st.dataframe(
        coefficient_df,
        use_container_width=True
    )

    if enable_prediction:

        if st.button(
            "Predict Rotational Speed"
        ):

            prediction = linear_model.predict([[
                air_temp,
                process_temp,
                torque,
                tool_wear
            ]])

            st.success(
                f"Predicted RPM: {round(prediction[0], 2)}"
            )
else:

    st.subheader(
        "Logistic Regression"
    )

    X_logistic = filtered_df[[
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]]

    y_logistic = filtered_df[
        "Machine failure"
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X_logistic,
        y_logistic,
        test_size=0.2,
        random_state=42
    )

    logistic_model = LogisticRegression(
        max_iter=1000
    )
    logistic_model.fit(
        X_train,
        y_train
    )   
    logistic_pred = logistic_model.predict(
        X_test
    )
    

    accuracy = accuracy_score(
        y_test,
        logistic_pred
    )

    st.metric(
        "Logistic Regression Accuracy",
        f"{round(accuracy * 100, 2)}%"
    )

    cm = confusion_matrix(
        y_test,
        logistic_pred
    )

    fig8 = ff.create_annotated_heatmap(
        z=cm,
        x=["No Failure", "Failure"],
        y=["No Failure", "Failure"],
        colorscale="Blues",
        showscale=True
    )

    fig8.update_layout(
        title="Logistic Regression Confusion Matrix",
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

    result_df = pd.DataFrame({
        "Result": [
            "Correct Prediction",
            "Wrong Prediction"
        ],
        "Count": [
            (y_test == logistic_pred).sum(),
            (y_test != logistic_pred).sum()
        ]
    })

    if enable_prediction:

        if st.button(
            "Predict Machine Failure"
        ):

            failure_prediction = logistic_model.predict([[
                air_temp,
                process_temp,
                rpm,
                torque,
                tool_wear
            ]])

    if enable_prediction:

        if st.button(
            "Predict Machine Failure"
        ):

            failure_prediction = logistic_model.predict([[
                air_temp,
                process_temp,
                rpm,
                torque,
                tool_wear
            ]])

            if failure_prediction[0] == 1:

                st.error(
                    "Machine Failure Predicted"
                )

            else:

                st.success(
                    "Machine Working Normally"
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

