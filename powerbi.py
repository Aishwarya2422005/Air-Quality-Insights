import streamlit as st
import sqlite3
from hashlib import sha256

# Database setup
def create_userdb():
    """Create the SQLite database and users table if not exists."""
    conn = sqlite3.connect("userdb.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    """Add a new user to the database."""
    conn = sqlite3.connect("userdb.db")
    cursor = conn.cursor()
    try:
        hashed_password = sha256(password.encode()).hexdigest()  # Hash the password
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def authenticate_user(username, password):
    """Authenticate a user against the database."""
    conn = sqlite3.connect("userdb.db")
    cursor = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    result = cursor.fetchone()
    conn.close()
    return result

# Initialize database
create_userdb()

# Set up page configuration
st.set_page_config(
    page_title="Air Quality Insights",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Background image URL
background_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqMYLS0l3uPO4flRmWfG7xmp1Y9YaHgBatzA&s"

st.markdown(
    f"""
    <style>
        /* Background styling */
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Arial', sans-serif;
        }}
        /* Title styling */
        h1 {{
            font-family: 'Dancing Script', cursive;
            color: #2c3e50;
            font-size: 60px;
            text-align: center;
            margin-bottom: 10px;
        }}
        p {{
            color: #34495e;
            font-size: 20px;
            text-align: center;
        }}
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            font-weight: bold;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6, [data-testid="stSidebar"] p {{
            color: white;
            font-weight: bold;
        }}
        /* Transparent background for login/signup forms */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: transparent !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent !important;
        }}
        .stTabs div[role="tabpanel"] {{
            background-color: rgba(255, 255, 255, 0.7) !important;
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(5px);
        }}
        /* Style for form inputs to match transparent background */
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(5px);
        }}
        .stButton > button {{
            background-color: rgba(44, 62, 80, 0.7) !important;
            color: white !important;
            border: none;
            backdrop-filter: blur(5px);
        }}
        .stButton > button:hover {{
            background-color: rgba(44, 62, 80, 0.9) !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Include Google Font
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Main content
if st.session_state.logged_in:
    # Dashboard after login
    st.markdown(
        """
        <h1>🌍 Air Quality Insights</h1>
        <p>Monitor, Analyze, and Improve Air Quality</p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
                <link href="https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap" rel="stylesheet">
                <style>
                    .custom-sans-serif {
                        font-family: 'Lato', sans-serif; /* Sans-serif font */
                        font-size: 30px; /* Adjust font size */
                        font-weight: bold; /* Make it bold for emphasis */
                        color: #2c3e50; /* Dark gray/blue color */
                        text-align: center; /* Center alignment */
                        margin-bottom: 20px;
                    }
                </style>
                <h2 class="custom-sans-serif">Welcome! Get insights into India’s air quality trends. </h2>  """, unsafe_allow_html=True)
    # Sidebar for Dashboard Navigation
    st.sidebar.title("📊 Dashboard Navigation")
    dashboard_links = {
        "Historical Trends": "https://app.powerbi.com/view?r=eyJrIjoiYzViNjE4YTAtZDc2Mi00MzY2LTkxYjUtZDI0NzM0M2JhOTUzIiwidCI6IjkzZTljMTgyLTdhOWMtNGI4YS04YzY1LTM3OTMyNDZlYzgzMyJ9",
        "Real-Time AQI Dashboard": "https://app.powerbi.com/view?r=eyJrIjoiNmU4MDY4ZDUtYzA1MS00MmE1LWIxNjItOTAwNzI4NjEwNDUzIiwidCI6IjkzZTljMTgyLTdhOWMtNGI4YS04YzY1LTM3OTMyNDZlYzgzMyJ9"
    }
    selected_dashboard = st.sidebar.radio("Choose a Dashboard", list(dashboard_links.keys()))
    st.markdown(
        f'<iframe src="{dashboard_links[selected_dashboard]}" width="100%" height="600px" frameborder="0" allowfullscreen></iframe>',
        unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

else:
    # Login/Signup Tabs
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # Login Tab
    with tab1:
        st.markdown(
            """
            <h1>🌍 Air Quality Insights</h1>
            <p>Access detailed air quality information across India.</p>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap" rel="stylesheet">
            <style>
                .custom-sans-serif {
                    font-family: 'Lato', sans-serif; /* Sans-serif font */
                    font-size: 30px; /* Adjust font size */
                    font-weight: bold; /* Make it bold for emphasis */
                    color: #2c3e50; /* Dark gray/blue color */
                    text-align: center; /* Center alignment */
                    margin-bottom: 20px;
                }
            </style>
            <h2 class="custom-sans-serif">LOGIN</h2>
        """, unsafe_allow_html=True)
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate_user(login_username, login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # Signup Tab
    with tab2:
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap" rel="stylesheet">
            <style>
                .custom-sans-serif {
                    font-family: 'Lato', sans-serif; /* Sans-serif font */
                    font-size: 30px; /* Adjust font size */
                    font-weight: bold; /* Make it bold for emphasis */
                    color: #2c3e50; /* Dark gray/blue color */
                    text-align: center; /* Center alignment */
                    margin-bottom: 20px;
                }
            </style>
            <h2 class="custom-sans-serif">SIGN UP</h2>
        """, unsafe_allow_html=True)
        signup_username = st.text_input("Username", key="signup_username")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Signup"):
            if add_user(signup_username, signup_password):
                st.success("Signup successful! You can now login.")
            else:
                st.error("Username already exists. Try another.")
