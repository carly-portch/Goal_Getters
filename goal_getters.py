import streamlit as st

# Step 1: Input Form for Partner 1
st.title("Goal Getters: Collaborative Goal Planner")
st.write("Plan your financial goals together!")

# Step 2: File Upload (for Partner 2)
uploaded_file = st.file_uploader("Upload your partner's goal file", type=["txt"])

# Initialize default variables for Partner 2
your_name = ""
partner_name = ""
goal_name = ""
total_goal = 50000
timeline_years = 5.0
split_percent = 50

# Function to clean the parsed data values
def clean_value(value, default_value, remove_chars=None):
    """
    Cleans the parsed value by removing specified characters and converting it to the appropriate type.
    Args:
    - value (str): The parsed value from the uploaded file.
    - default_value: The default value to return if cleaning fails.
    - remove_chars (list): A list of characters to remove from the value.
    
    Returns:
    - The cleaned value, converted to the appropriate type (int or float).
    """
    if not value:
        return default_value
    
    # Remove unwanted characters
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


# Step 3: Handle file upload and parse data if file is uploaded
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    
    # Parse the content of the uploaded file
    try:
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
        
        # Display pre-filled data in the input fields for Partner 2 to adjust
        st.write("Partner's information has been pre-filled. Adjust as needed.")
        
    except Exception as e:
        st.error(f"Error parsing the uploaded file: {e}")

# Step 4: Allow Partner 2 to adjust and re-save
your_name = st.text_input("Your Name", value=your_name)
partner_name = st.text_input("Partner's Name", value=partner_name)
goal_name = st.text_input("Goal (e.g., Buy a house)", value=goal_name)
total_goal = st.number_input("Total Goal Amount ($)", min_value=0, value=total_goal, step=1000)
timeline_years = st.number_input("Timeline (Years)", min_value=0.5, value=timeline_years, step=0.5)
split_percent = st.slider("Your Contribution (%)", min_value=0, max_value=100, value=split_percent)

# Step 5: Save & Generate File (Partner 2's Data after adjustments)
if st.button("Save & Generate File"):
    # Prepare content for the text file (adjusted by Partner 2)
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
            label="Download Your Updated Goal Planner",
            data=file,
            file_name="goal_planner_output.txt",
            mime="text/plain"
        )
    
    st.success("Your goal planner file has been generated! Download it and share with your partner.")
