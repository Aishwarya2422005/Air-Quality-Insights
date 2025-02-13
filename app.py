import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import bcrypt

# Initialize SQLite database connection
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# Create a table for storing users
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
"""
)
conn.commit()


# Function to add a user to the database
def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()


# Function to verify user credentials
def verify_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hash = result[0]
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    return False


# Set page configuration
st.set_page_config(
    layout="wide", page_title="Dashboard | Air Quality Index", page_icon="📊"
)

hide_st_style = """ 
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Check if the user is logged in (session state)
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

# Sidebar for navigation

if not st.session_state.user_logged_in:
    # Show only Login/Signup when the user is not logged in

    selected = option_menu(
        menu_title="Welcome!", options=["Login/Signup"], icons=["key"]
    )
else:
    # Show Dashboard and Connect on LinkedIn once logged in
    with st.sidebar:
        selected = option_menu(
            menu_title="Welcome!",
            options=["Dashboard", "Connect on LinkedIn", "Logout"],
            icons=["arrow-right-circle", "envelope", "key"],
        )

# Login/Signup Page
if selected == "Login/Signup":
    menu = ["Login", "Signup"]
    choice = st.selectbox("Select an option", menu)

    # Login Form
    if choice == "Login":
        st.subheader("Login to Your Account")
        with st.form(key="login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")

            if submit_button:
                if verify_user(username, password):
                    st.success("Login successful!")
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.rerun()  # Refresh to go to the Dashboard
                else:
                    st.error("Invalid username or password.")

    # Signup Form
    if choice == "Signup":
        st.subheader("Create a New Account")
        with st.form(key="signup_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button(label="Signup")

            if submit_button:
                if password == confirm_password:
                    try:
                        add_user(username, password)
                        st.success("Signup successful! You can now log in.")
                    except sqlite3.IntegrityError:
                        st.error(
                            "Username already exists. Please choose a different username."
                        )
                else:
                    st.error("Passwords do not match.")

# Dashboard page (only for logged-in users)
if selected == "Dashboard" and st.session_state.user_logged_in:
    st.title("ClearView: Interactive Air Quality Insights")
    st.markdown(
        """
    The **Air Quality Index (AQI) Visualization** project provides an interactive and insightful dashboard designed to help users explore and analyze air quality data across **India**. The dashboard leverages data from 2020 to 2022 to offer a comprehensive view of air quality trends and the impact of key pollutants across various Indian cities. It serves as a valuable tool for **environmental analysts**, **policymakers**, and the **general public**, enabling them to make data-driven decisions related to air quality management and public health.

    #### Key Features of the Dashboard:
    - **AQI Trends Over Time**: Visualize how air quality has evolved across India over the years, with detailed temporal analysis of AQI levels.
    - **Monthly Trends in AQI**: Observe seasonal variations in air quality and identify months with high pollution.
    - **Contribution of Key Pollutants**: Understand the role of major pollutants—such as **PM2.5**, **PM10**, **CO**, **SO2**, **NO2**, **O3**, and **CO**—in influencing the AQI in different regions.
    - **City-Specific Analysis**: Dive into specific cities to analyze localized trends and pollution sources.
    - **Interactive Visualizations**: Easily explore different aspects of air quality data through dynamic charts, graphs, and maps.
    - **Trend Comparisons**: Compare AQI trends across cities, states, or regions for more in-depth analysis.

    This platform empowers users to track air quality fluctuations, identify key sources of pollution, and gain a deeper understanding of regional disparities. Whether for **policy development**, **environmental monitoring**, or **public awareness**, this dashboard is a vital tool for addressing the challenges posed by air pollution in India."""
    )
    st.header("", divider=True)
    # Add the PowerBI iframe

    iframe_code = """<iframe title="AQI" width="1020" height="950" src="https://app.powerbi.com/view?r=eyJrIjoiNzNmZWFlOTEtYjRhYi00OTIxLWFiZTQtOGI5YWQwYjFlNjcyIiwidCI6IjY5YmQ5ODlhLTkyN2QtNDRlZS05ZWRkLTYwOWFjZmY4MmY1MiJ9" frameborder="0" allowFullScreen="true"></iframe>"""

    st.components.v1.html(iframe_code, height=600)

    # Conclusion Section
    st.title("Conclusion")
    st.markdown(
        """
    The AQI trends from **2020-2022** emphasize the urgent need to address air pollution, especially in urban regions, and implement actionable plans for a **cleaner, greener, and healthier future** for India.

    To tackle this challenge, the following actions should be prioritized:

    - **Enforcing stricter air quality standards** on industries and vehicle emissions to reduce pollutants.
    - **Developing green spaces** in urban areas to absorb pollutants and improve air quality.
    - **Raising public awareness** about the health risks of poor air quality and promoting environmentally-friendly practices.
    - **Implementing predictive models** to anticipate pollution spikes and take preventive actions ahead of time.

    By taking these steps, we can ensure a healthier environment for future generations and significantly improve the air quality in India.
    """
    )

# CONNECT PAGE STARTS HERE

if selected == "Connect on LinkedIn":
    st.markdown(
        """
        <style>
        .custom-button {
            background-color: #f0f0f0;  /* Light gray background */
            color: #333;  /* Dark text color */
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;  /* Rounded corners */
            border: 1px solid #ccc;  /* Light gray border */
            box-shadow: none;  /* No shadow */
            width: 100%;
            cursor: pointer;
            text-align: left;
            display: inline-block;
            text-decoration: none;
        }
        .custom-button:hover {
            background-color: #e1e1e1;  /* Slightly darker gray on hover */
        }
        .custom-button:active {
            background-color: #ccc;  /* Darker gray when clicked */
        }
    </style>
    """, unsafe_allow_html=True
    )

    st.markdown(
        """
        I'm Aishwarya S, a passionate student coming from a Computer Science background. I enjoy connecting with like-minded people, exchanging ideas, and collaborating on exciting projects. Feel free to reach out to me through any of the channels below.
        """
    )

    st.markdown("---")

    st.subheader("Let's Connect!")
    st.markdown(
        """
        You can reach me through the following platforms:
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<a href="https://www.linkedin.com/in/aishwarya-s-b99b90268/" target="_blank" class="custom-button">🤝 LinkedIn</a>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<a href="mailto:s.aishwarya2412@gmail.com" target="_blank" class="custom-button">📩 Email</a>',
            unsafe_allow_html=True
        )
    st.markdown("---")

footer_html = """
<div style="background-color:#f0f2f6; padding:20px; text-align:center; border-radius:20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
    <p style="margin: 0; font-size: 16px;">&copy; Infosys Springboard Internship 5.0.  All rights reserved.<br> 
    Created with ❤️ by Aishwarya S

</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

# CONNECT PAGE ENDS HERE

# Logout

if selected == "Logout" and st.session_state.user_logged_in:
    st.session_state.user_logged_in = False
    st.session_state.username = None
    st.success("Logout successful! You have been logged out.")
    st.rerun()
