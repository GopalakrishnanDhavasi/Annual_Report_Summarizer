import streamlit as st
import hashlib
import os

def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    return get_hashed_password(password) == hashed_password

def login():
    """Simple username-password login using Streamlit session state."""
    # Backwards-compatible wrapper for container-aware login UI.
    return login_ui()


def login_ui(container=None):
    """Render the login UI into the given Streamlit container (a column or st).

    Returns True when the user is authenticated. If container is None, uses the
    top-level `st` object (maintains compatibility with existing code).
    """
    cs = container if container is not None else st

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Input keys are namespaced so multiple renders won't conflict.
    username = cs.text_input("Username", key="login_username")
    password = cs.text_input("Password", type="password", key="login_password")

    # Load stored credentials
    correct_username = os.getenv("APP_USERNAME", "admin")
    correct_password_hash = get_hashed_password(os.getenv("APP_PASSWORD", "1234"))

    if cs.button("Login", key="login_button"):
        if username == correct_username and verify_password(password, correct_password_hash):
            st.session_state.authenticated = True
            cs.success("Login successful!")
            # Rerun the app so callers see the updated session state immediately.
            st.rerun()
        else:
            cs.error("Invalid credentials. Please try again.")

    # Simple social buttons (placeholders) — they don't authenticate but are UI affordances.
    cs.markdown("---")
    col1, col2 = cs.columns(2)
    if col1.button("Google", key="google_signin"):
        cs.info("Google sign-in not configured in this demo.")
    if col2.button("Facebook", key="facebook_signin"):
        cs.info("Facebook sign-in not configured in this demo.")

    return st.session_state.authenticated

def logout():
    st.session_state.authenticated = False
    st.rerun()
