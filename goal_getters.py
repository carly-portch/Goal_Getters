import streamlit as st
import math

def calculate_monthly_contributions(total_goal, timeline_years, split_percent):
    months = timeline_years * 12
    partner_1_contribution = (split_percent / 100) * total_goal / months
    partner_2_contribution = ((100 - split_percent) / 100) * total_goal / months
    return partner_1_contribution, partner_2_contribution

# App Title
st.title("Goal Getters: Collaborative Financial Goal Planner")
st.write("Plan your big goals together, align on contributions, and make your dreams a reality!")

# Step 1: Input Goal Details
st.header("Step 1: Define Your Goal")
goal_name = st.text_input("What is your goal?", "e.g., Buy a house")
total_goal = st.number_input("Total savings needed ($)", min_value=0, value=50000, step=1000)
timeline_years = st.number_input("Timeline to save (years)", min_value=0.5, value=5.0, step=0.5)
split_percent = st.slider("What percentage of the total will you contribute?", min_value=0, max_value=100, value=50)

# Calculate Contributions
partner_1_monthly, partner_2_monthly = calculate_monthly_contributions(total_goal, timeline_years, split_percent)

# Display Calculations
st.subheader("Suggested Monthly Contributions")
st.write(f"Your monthly contribution: **${partner_1_monthly:.2f}**")
st.write(f"Your partner's monthly contribution: **${partner_2_monthly:.2f}**")

# Step 2: Partner Review and Adjustments
st.header("Step 2: Review and Adjust")
st.write("Share your plan with your partner for feedback. They can adjust the details below.")
adjusted_split = st.slider("Adjust the percentage split (Partner 1 %)", min_value=0, max_value=100, value=split_percent)
adjusted_timeline_years = st.number_input("Adjust the timeline to save (years)", min_value=0.5, value=timeline_years, step=0.5)

# Recalculate Based on Adjustments
adjusted_partner_1_monthly, adjusted_partner_2_monthly = calculate_monthly_contributions(total_goal, adjusted_timeline_years, adjusted_split)

# Display Adjusted Contributions
st.subheader("Adjusted Monthly Contributions")
st.write(f"Your adjusted monthly contribution: **${adjusted_partner_1_monthly:.2f}**")
st.write(f"Your partner's adjusted monthly contribution: **${adjusted_partner_2_monthly:.2f}**")

# Finalize Plan
if st.button("Finalize Plan"):
    st.success("Your plan is finalized! You and your partner are aligned and ready to start saving.")

