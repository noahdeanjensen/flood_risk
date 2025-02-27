import streamlit as st
from utils.auth import check_auth, init_auth
from utils.db import init_database, init_admin
from views import home, assessment, dashboard, documentation, admin

# Page configuration
st.set_page_config(
    page_title="Stormwater Infrastructure Assessment",
    page_icon="🌧️",
    layout="wide"
)

def main():
    # Initialize authentication and database
    init_auth()
    init_database()

    # Initialize admin user if needed
    if not st.session_state.get("initialized", False):
        init_admin()
        st.session_state.initialized = True

    # Sidebar navigation
    st.sidebar.title("Navigation")

    if not st.session_state.get("authenticated", False):
        check_auth()
        return

    pages = {
        "Home": home.show,
        "Assessment": assessment.show,
        "Dashboard": dashboard.show,
        "Documentation": documentation.show
    }

    # Add admin page if user is admin
    if st.session_state.get("is_admin", False):
        pages["Admin Panel"] = admin.show

    page = st.sidebar.selectbox("Go to", list(pages.keys()))
    pages[page]()

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.session_state.user_id = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()