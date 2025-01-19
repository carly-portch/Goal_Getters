import streamlit as st
import urllib.parse

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

if st.button("Save & Send"):
    # Encode data into URL
    params = {
        "your_name": your_name,
        "partner_name": partner_name,
        "goal_name": goal_name,
        "total_goal": total_goal,
        "timeline_years": timeline_years,
        "split_percent": split_percent,
    }
    query_string = urllib.parse.urlencode(params)
    link = f"{st.experimental_get_query_params()}?{query_string}"
    
    # Display the link for sharing
    st.success("Link generated! Share this with your partner:")
    st.write(link)

# Step 2: Load Partner 1's Data if URL contains pre-filled parameters
st.header("Review Partner 1's Plan")
query_params = st.experimental_get_query_params()
if query_params:
    st.write("Pre-filled details from Partner 1:")
    st.write(f"Your Name: {query_params.get('your_name', [''])[0]}")
    st.write(f"Partner's Name: {query_params.get('partner_name', [''])[0]}")
    st.write(f"Goal: {query_params.get('goal_name', [''])[0]}")
    st.write(f"Total Goal: ${query_params.get('total_goal', [''])[0]}")
    st.write(f"Timeline: {query_params.get('timeline_years', [''])[0]} years")
    st.write(f"Contribution Split: {query_params.get('split_percent', [''])[0]}%")
