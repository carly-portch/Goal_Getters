import streamlit as st
import os

# Step 1: Input Form for Partner 1
st.title("Goal Getters: Collaborative Goal Planner")
st.write("Plan your financial goals together!")

# Form Inputs
your_name = st.text_input("Your Name")
partner_name = st.text_input("Partner's Name")
goal_name = st.text_input("Goal (e.g., Buy a house)", "")
total_goal = st.number_input("Total Goal Amount ($)", min_value=0, value=50000, step=1000)
timeline_years = st.number_input("Timeline (Years)", min_value=0.5, value=5.0, step=0.5)
split_percent = st.slider("Your Contribution (%)", min_value=0, max_value=100, value=50)

if st.button("Save & Generate File"):
    # Prepare content for the text file
    file_content = f"""Goal Getters - Collaborative Goal Planner
-----------------------------------------
Partner 1's Information:
Your Name: {your_name}
Partner's Name: {partner_name}
Goal: {goal_name}
Total Goal: ${total_goal}
Timeline: {timeline_years} years
Contribution Split: {split_percent}%

Calculated Details:
Your Contribution: ${total_goal * split_percent / 100}
Partner's Contribution: ${total_goal * (100 - split_percent) / 100}
"""
    
    # Write content to a temporary text file
    temp_file_path = "/tmp/goal_planner_output.txt"  # Streamlit can use /tmp to store temp files
    with open(temp_file_path, "w") as file:
        file.write(file_content)
    
    # Offer the file as a download
    with open(temp_file_path, "rb") as file:
        st.download_button(
            label="Download Your Goal Planner",
            data=file,
            file_name="goal_planner_output.txt",
            mime="text/plain"
        )
    
    st.success("Your goal planner file has been generated! Download it and share with your partner.")
