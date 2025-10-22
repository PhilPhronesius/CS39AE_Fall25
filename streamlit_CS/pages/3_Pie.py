import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the page
st.title("3_Pie - Pie Chart Visualization")

# Read the CSV file
data = pd.read_csv('assets/data/pie_demo.csv')

# Check if the CSV has been read correctly
st.write("Data from CSV:", data)

# Generate a pie chart
fig, ax = plt.subplots()
ax.pie(data['Value'], labels=data['Category'], autopct='%1.1f%%', startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.axis('equal')

# Show the pie chart in Streamlit
st.pyplot(fig)
