import streamlit as st
import os
from utils import *
from bimamitra_db import *

# Function to simulate user authentication using environment variable
def authenticate(username, password):
    # Fetch the user list from the environment variable, handling spaces and newlines
    user_list_env = os.getenv("USER_LIST", "")  # Default to empty string if not set
    users = [u.strip().split(":") for u in user_list_env.split(",") if u.strip()]

    # Check if the provided credentials match any user in the list
    for user, pwd in users:
        if username == user.strip() and password == pwd.strip():
            st.session_state['username']=username
            return True
    return False

# Login Page
def login_page():
    st.header("Login Page")
    with st.form("Login Form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Login button
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if authenticate(username, password):
                st.success(f"Welcome '{username}', You are successfully logged in!")
                st.success("Tap \'Login\' to continue")
                st.session_state['authenticated'] = True
            else:
                st.error("The username or password you have entered is incorrect.")


def userinfo():
    st.sidebar.write(f"User: \'{st.session_state.get('username', '')}\'")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()




# Main Page
def main_page():
  
    # Display user information and logout button
    userinfo()
    
    # Retrieve user query
    query = st.text_area("Enter query here.. 👇🏻", key='question')
    resposne = None

    # Check if 'Get Answer' button is clicked
    if st.button("Get Answer"):
        if query:
            # Generate response
            with st.spinner("Generating Response"):
                response = generate_response_rag(query)
                st.write(response)
                udpate_database(st.session_state["username"],
                                query, response)
                
        else:
            st.error("Provide the query first")

    # if resposne is not None:
        # rating = st.slider("Rate this response", 0, 5, 2)
        # if st.button("Submit rating"):
        #     st.success(udpate_database(st.session_state["username"], 
        #                                 query, response, rating))

        
    
def page_config():
    st.set_page_config(
        page_title="🛡️ BimaMitra App",
        page_icon=":smiley:",
        # layout="wide",
        initial_sidebar_state="auto"
    )
    st.title("🔬 BimaMitra Chatbot")
    

def main():

    # configure page
    page_config()

    # Use session state to keep track of authentication status
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username'] = None


    if not st.session_state['authenticated']:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main()
