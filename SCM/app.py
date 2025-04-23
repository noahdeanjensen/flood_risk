import streamlit as st
import base64
from utils.auth import check_auth, init_auth
from utils.db import init_database, init_admin
from views import home, assessment, dashboard, documentation, admin, projects

# Page configuration
st.set_page_config(
    page_title="Stormwater Infrastructure Assessment",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide Streamlit's default menu and footer and add custom styles
def apply_custom_styles():
    custom_styles = """
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom styles for full-height image */
    .full-height-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
    }
    
    /* Remove deprecation yellow box */
    div[data-deprecation-warning="true"] {
        display: none;
    }
    </style>
    """
    st.markdown(custom_styles, unsafe_allow_html=True)

def main():
    # Initialize authentication and database
    init_auth()
    init_database()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Add demo-ready styling
    st.markdown("""
    <style>
    /* Add professional styling for demo */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Style headers for better appearance */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Make buttons more modern */
    button[kind="primary"] {
        background-color: #3498db;
        border-radius: 6px;
    }
    
    /* Style metrics for cleaner look */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    
    /* Make tabs cleaner */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 4px 4px 0 0;
    }
    
    /* Improve dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Center the sidebar logo */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-left: auto;
        margin-right: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize admin user if needed
    if not st.session_state.get("initialized", False):
        init_admin()
        st.session_state.initialized = True

    # Login page if not authenticated
    if not st.session_state.get("authenticated", False):
        # Apply additional styling for login page
        st.markdown("""
        <style>
        /* Remove page margins and padding for full-width appearance */
        .main .block-container {
            max-width: 100%;
            padding: 0;
            margin: 0;
        }
        
        /* Improve padding for login container */
        .login-container {
            padding: 2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100vh;
        }
        
        /* Center and style the login form elements */
        div[data-testid="stVerticalBlock"] {
            margin: 0 auto;
        }
        
        /* Style text inputs */
        div[data-testid="stTextInput"] > div:first-child {
            border-radius: 8px;
        }
        
        /* Remove header margins */
        h2, h3 {
            margin-top: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create a layout with two equal columns
        login_col1, login_col2 = st.columns([1, 1])
        
        # Left column with full-height image using custom HTML
        with login_col1:
            # Use HTML to get a full-height image with better margins
            st.markdown(f"""
            <div style="position:relative; height:100vh; overflow:hidden; margin:-4rem -1rem -2rem -4rem;">
                <img src="data:image/svg+xml;base64,{base64.b64encode(open('doc_assets/images/stormwater_login.svg', 'rb').read()).decode()}" 
                     style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover; border-right:1px solid rgba(255,255,255,0.1);" />
            </div>
            """, unsafe_allow_html=True)
        
        # Right column with login form - with better centering
        with login_col2:
            # Create a container with explicit vertical centering
            st.markdown("""
            <div style="height:20vh"></div>
            """, unsafe_allow_html=True)
            
            # Centered content with proper margins
            with st.container():
                # Center the logo image
                col_a, col_b, col_c = st.columns([1, 1, 1])
                with col_b:
                    st.image("generated-icon.png", width=100)
                
                # Add some space between logo and form
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                
                # Wrap login form in container with better margins
                col_wrapper1, col_wrapper2, col_wrapper3 = st.columns([1, 3, 1])
                with col_wrapper2:
                    # Display login form
                    check_auth()
        return

    # Main navigation sidebar with centered logo and improved styling
    with st.sidebar:
        # Centered logo with custom styling
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{}" width="120" style="margin: 0 auto; display: block; padding: 10px; border-radius: 50%; background-color: rgba(255,255,255,0.8);">
            <h2 style="margin-top: 10px; color: #2c3e50; font-size: 1.5em; font-weight: 600;">Stormwater Assessment</h2>
        </div>
        """.format(base64.b64encode(open('generated-icon.png', 'rb').read()).decode()), unsafe_allow_html=True)
        
        # Clean divider
        st.markdown('<hr style="margin: 0; margin-bottom: 20px; border: none; height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.1), rgba(0,0,0,0));">', unsafe_allow_html=True)
        
        # Navigation title with icon
        st.markdown('<p style="font-size: 1.1em; font-weight: 600; margin-bottom: 10px;">📋 NAVIGATION</p>', unsafe_allow_html=True)

        # Create navigation container with cleaner design
        with st.container():
            pages = {
                "🏠 Dashboard": dashboard.show,
                "📊 Projects": projects.show,
                "📝 Assessment": assessment.show,
                "📚 Documentation": documentation.show
            }

            # Add admin page if user is admin
            if st.session_state.get("is_admin", False):
                pages["⚙️ Admin"] = admin.show

            # Navigation buttons with enhanced styling
            selected_page = None
            for page_name, page_func in pages.items():
                if st.button(
                    page_name,
                    use_container_width=True,
                    key=f"nav_{page_name}"
                ):
                    selected_page = page_func

            # Clean divider before user section
            st.markdown('<hr style="margin: 20px 0; border: none; height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.1), rgba(0,0,0,0));">', unsafe_allow_html=True)
            
            # User section with better styling
            username = st.session_state.get('username', 'User')
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 8px; background-color: rgba(52, 152, 219, 0.1); margin-bottom: 10px;">
                <p style="margin: 0; display: flex; align-items: center;">
                    <span style="background-color: #3498db; color: white; border-radius: 50%; width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">
                        {username[0].upper()}
                    </span>
                    <span style="font-weight: 500;">{username}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Styled logout button
            if st.button("🚪 Sign Out", use_container_width=True, type="primary"):
                st.session_state.authenticated = False
                st.session_state.is_admin = False
                st.session_state.user_id = None
                st.rerun()

    # Main content area
    with st.container():
        if selected_page:
            selected_page()
        else:
            dashboard.show()  # Default to dashboard

if __name__ == "__main__":
    main()