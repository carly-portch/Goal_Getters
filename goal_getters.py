import streamlit as st

# Initialize default values with explicit types
your_name = "Carly"
partner_name = "Jim"
goal_name = "Buy a House"
total_goal = 50000.0  # Ensure this is a float
timeline_years = 5.0  # Ensure this is a float
split_percent = 50  # Default percentage (int)
flip_percent = 50  # Default flipped percentage (int)

# Function to clean and parse data from uploaded file
def clean_value(value, default_value, remove_chars=None):
    if not value:
        return default_value
    
    if remove_chars:
        for char in remove_chars:
            value = value.replace(char, "")
    
    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        return default_value


# File upload handling
uploaded_file = st.file_uploader("Upload your partner's goal file", type=["txt"])

# Step 1: Handle file upload and parse data if file is uploaded
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    
    try:
        # Parse the content of the uploaded file
        lines = content.splitlines()
        parsed_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in lines if ":" in line}
        
        # Repopulate the fields with the parsed data from the uploaded file
        your_name = parsed_data.get("Your Name", your_name)
        partner_name = parsed_data.get("Partner's Name", partner_name)
        goal_name = parsed_data.get("Goal", goal_name)
        
        # Clean and parse total goal to float (remove '$' and commas)
        total_goal = clean_value(parsed_data.get("Total Goal", ""), total_goal, remove_chars=["$", ","])
        
        # Clean and parse timeline_years (remove 'years')
        timeline_years = clean_value(parsed_data.get("Timeline", ""), timeline_years, remove_chars=["years"])
        
        # Clean and parse split_percent (remove '%')
        split_percent = clean_value(parsed_data.get("Contribution Split", ""), split_percent, remove_chars=["%"])
        
        # Flip the split percent for the second partner (complementary)
        flip_percent = 100 - split_percent
        
        # Display message
        st.write(f"{your_name} has filled out the goal planner. You can make edits in the second column.")
        
    except Exception as e:
        st.error(f"Error parsing the uploaded file: {e}")
else:
    flip_percent = 50  # Default value if no file is uploaded

# Step 2: Set up columns for Partner 1 and Partner 2
col1, col2 = st.columns(2)

with col1:
    # Left Column: Display Partner 1's Data (with inputs above the sliders)
    st.header(f"{your_name}'s Information")
    
    # Display input fields for Partner 1 (goal name, total goal, timeline)
    goal_name_input = st.text_input("Goal Name", value=goal_name, key="goal_name_input")
    total_goal_input = st.number_input("Total Goal Amount ($)", min_value=0.0, value=float(total_goal), step=1000.0)
    timeline_years_input = st.number_input("Timeline (Years)", min_value=1, value=int(timeline_years), step=1)
    
    # Display the contribution slider and information for Partner 1 (left column)
    split_percent_1 = st.slider(f"{your_name}'s Contribution (%)", min_value=0, max_value=100, value=split_percent, key="split_percent_1")
    partner_1_contribution = (total_goal * split_percent_1 / 100)
    monthly_partner_1_contribution = partner_1_contribution / (timeline_years_input * 12)
    
    # Display the percentage and dollar amount for Partner 1
    st.write(f"**{your_name}'s Contribution**: {split_percent_1}%")
    st.write(f"**{your_name}'s Monthly Contribution**: ${monthly_partner_1_contribution:.2f}")
    
    st.write(f"**{partner_name}'s Contribution**: {100 - split_percent_1}%")
    partner_2_contribution = total_goal - partner_1_contribution
    monthly_partner_2_contribution = partner_2_contribution / (timeline_years_input * 12)
    
    # Display the percentage and dollar amount for Partner 2 (left column)
    st.write(f"**{partner_name}'s Monthly Contribution**: ${monthly_partner_2_contribution:.2f}")
    
with col2:
    # Right Column: Display Partner 2's Data (Editable for Partner 2)
    st.header(f"{partner_name}'s Information")
    
    # Display input fields for Partner 2 (goal name, total goal, timeline)
    goal_name_input_2 = st.text_input("Goal Name", value=goal_name, key="goal_name_input_2")
    total_goal_input_2 = st.number_input("Total Goal Amount ($)", min_value=0.0, value=float(total_goal), step=1000.0)
    timeline_years_input_2 = st.number_input("Timeline (Years)", min_value=1, value=int(timeline_years), step=1)
    
    # Display the contribution slider and information for Partner 2 (right column)
    split_percent_2 = st.slider(f"{partner_name}'s Contribution (%)", min_value=0, max_value=100, value=flip_percent, key="split_percent_2")
    partner_2_contribution = (total_goal * split_percent_2 / 100)
    monthly_partner_2_contribution = partner_2_contribution / (timeline_years_input_2 * 12)
    
    # Display the percentage and dollar amount for Partner 2
    st.write(f"**{partner_name}'s Contribution**: {split_percent_2}%")
    st.write(f"**{partner_name}'s Monthly Contribution**: ${monthly_partner_2_contribution:.2f}")
    
    st.write(f"**{your_name}'s Contribution**: {100 - split_percent_2}%")
    partner_1_contribution = total_goal - partner_2_contribution
    monthly_partner_1_contribution = partner_1_contribution / (timeline_years_input_2 * 12)
    
    # Display the percentage and dollar amount for Partner 1 (right column)
    st.write(f"**{your_name}'s Monthly Contribution**: ${monthly_partner_1_contribution:.2f}")

# Step 3: Comparison at the bottom (aligning both partners for easy comparison)
st.subheader("Contribution Comparison")

# Left column contributions (from first partner)
st.write(f"{your_name}'s Contribution: {split_percent_1}% → ${monthly_partner_1_contribution:.2f} monthly")
st.write(f"{partner_name}'s Contribution: {100 - split_percent_1}% → ${monthly_partner_2_contribution:.2f} monthly")

# Right column contributions (from second partner, editable)
st.write(f"{partner_name}'s Contribution: {split_percent_2}% → ${monthly_partner_2_contribution:.2f} monthly")
st.write(f"{your_name}'s Contribution: {100 - split_percent_2}% → ${monthly_partner_1_contribution:.2f}")
