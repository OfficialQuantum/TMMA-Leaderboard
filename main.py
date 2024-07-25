import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Function to get today's date as a string
def get_today_date_str():
    return datetime.now().strftime('%Y-%m-%d')

# Function to get the CSV file name for a given date
def get_csv_filename(date_str):
    return f'leaderboard_{date_str}.csv'

# Function to load data from CSV
def load_data(date_str):
    filename = get_csv_filename(date_str)
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=['Name', 'Hours', 'Minutes', 'Total_Minutes'])

# Function to save data to CSV
def save_data(df, date_str):
    filename = get_csv_filename(date_str)
    df.to_csv(filename, index=False)

# Get list of existing leaderboard files
def get_existing_dates():
    files = os.listdir('.')
    dates = [f.replace('leaderboard_', '').replace('.csv', '') for f in files if f.startswith('leaderboard_') and f.endswith('.csv')]
    return sorted(dates)

# Load data for a specific date
def load_leaderboard_for_date(selected_date):
    return load_data(selected_date)

# Streamlit app
st.set_page_config(page_title="Daily Leaderboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding-left: 15%;
        padding-right: 15%;
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stButton {
        max-width: 500px;
        margin: auto;
    }
    .stForm {
        max-width: 400px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title('The Muslim Men Assembly')
st.markdown("Welcome to the Daily Leaderboard app!")

col_1, col_2, col_3, col_4 = st.columns([2, 2, 1, 3])
# Select date
existing_dates = get_existing_dates()
with col_3:
    selected_date = st.selectbox('Select date', options=existing_dates + [get_today_date_str()])

# Load data for the selected date
df = load_leaderboard_for_date(selected_date)

# Display leaderboard
st.subheader(f'Leaderboard for {selected_date}')
st.dataframe(df, width=800, height=300)

st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 1])
# Only allow adding players for today's leaderboard
if selected_date == get_today_date_str():
    with col1:
        st.markdown("<h5>Add New Data</h5>", unsafe_allow_html=True)
        with st.form("add_player_form"):
            cols = st.columns(3)
            col4, col5, col6 = st.columns([3, 1, 1])
            name = col4.text_input('Name')
            hours = col5.number_input('Hours', min_value=0, step=1)
            minutes = col6.number_input('Minutes', min_value=0, max_value=59, step=1)
            submit_button = st.form_submit_button(label='Add Player')

            if submit_button:
                total_minutes = hours * 60 + minutes
                new_data = pd.DataFrame({'Name': [name], 'Hours': [hours], 'Minutes': [minutes], 'Total_Minutes': [total_minutes]})
                df = pd.concat([df, new_data], ignore_index=True)
                df = df.sort_values(by='Total_Minutes').reset_index(drop=True)
                save_data(df, selected_date)
                st.success(f"Player {name} with time {hours} hours and {minutes} minutes (total {total_minutes} minutes) added to the leaderboard.")
                st.experimental_rerun()
else:
    st.warning('You can only add new players to today\'s leaderboard.')

st.markdown("<br><br>", unsafe_allow_html=True)
# Allow deleting players from today's leaderboard
col_01, col_02, col_03 = st.columns([3, 4, 4])
if selected_date == get_today_date_str() and not df.empty:
    with col_01:
        st.markdown("<h5>Delete Data</h5>", unsafe_allow_html=True)
        player_to_remove = st.selectbox('Select player to remove', options=df['Name'])
        if st.button('Remove Player'):
            df = df[df['Name'] != player_to_remove]
            save_data(df, selected_date)
            st.success(f"Player {player_to_remove} has been removed from the leaderboard.")
            st.experimental_rerun()
