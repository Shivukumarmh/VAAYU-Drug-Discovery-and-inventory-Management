import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample dataframe with manual data
data = {
    "Disease": ["Cancer", "Dengue", "Alzheimer's", "Acetylcholinesterase"],
    "Current Drug Supply (Units)": [10000, 15000, 12000, 8000],
    "Current Market Demand (Units)": [12000, 14000, 11000, 9000],
}

df = pd.DataFrame(data)

# Streamlit app
st.title("Drug Demand Forecasting")

st.sidebar.header("Input Data")

# User input for data
st.sidebar.subheader("Edit Drug Supply and Demand")

for disease in df["Disease"]:
    df.loc[df["Disease"] == disease, "Current Drug Supply (Units)"] = st.sidebar.number_input(
        f"Enter current drug supply for {disease}", value=int(df[df["Disease"] == disease]["Current Drug Supply (Units)"].values[0])
    )
    df.loc[df["Disease"] == disease, "Current Market Demand (Units)"] = st.sidebar.number_input(
        f"Enter current market demand for {disease}", value=int(df[df["Disease"] == disease]["Current Market Demand (Units)"].values[0])
    )

# Calculate the drug deficit or surplus
df["Deficit/Surplus (Units)"] = df["Current Market Demand (Units)"] - df["Current Drug Supply (Units)"]

# Display the dataframe
st.write("### Drug Supply and Demand Data")
st.dataframe(df)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot current drug supply and market demand
df.plot(kind='bar', x='Disease', y=['Current Drug Supply (Units)', 'Current Market Demand (Units)'], ax=ax)
ax.set_title("Drug Supply vs Market Demand")
ax.set_ylabel("Units")
ax.set_xlabel("Disease")

# Highlight deficits
for i, row in df.iterrows():
    if row["Deficit/Surplus (Units)"] > 0:
        ax.text(i, row["Current Market Demand (Units)"] + 500, f"+{row['Deficit/Surplus (Units)']}", ha='center', color='red')

# Display plot
st.pyplot(fig)

# Show deficit or surplus information
st.write("### Drug Deficit/Surplus")
st.dataframe(df[["Disease", "Deficit/Surplus (Units)"]])

# Add interactive element for more information
st.sidebar.subheader("More Information")
selected_disease = st.sidebar.selectbox("Select Disease", df["Disease"].tolist())
selected_data = df[df["Disease"] == selected_disease]
st.write(f"### {selected_disease} Details")
st.dataframe(selected_data)