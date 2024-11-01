import pandas as pd
import streamlit as st

if 'users' not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=['username', 'email', 'password', 'is_admin'])

    # Create data for the admin user and a non-super user for demo
    users = pd.DataFrame([
        {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'is_admin': True},
        {'username': 'user', 'email': 'user@example.com', 'password': 'user', 'is_admin': False}
    ])

    st.session_state.users = pd.concat([st.session_state.users, users], ignore_index=True)

if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=['id', 'title', 'description', 'timeline', 'expected_impact'])

if 'feedback' not in st.session_state:
    st.session_state.feedback = pd.DataFrame(columns=['project_id', 'username', 'rating', 'comment'])

if 'current_user' not in st.session_state:
    st.session_state.current_user = None


# Authentication functions
def login(username, password):
    user = st.session_state.users[
        (st.session_state.users['username'] == username) &
        (st.session_state.users['password'] == password)
        ]
    if not user.empty:
        st.session_state.current_user = user.iloc[0]
        return True
    return False


def logout():
    st.session_state.current_user = None
    st.session_state.page = "home"


# Page functions
def home_page():
    st.title("Community Feedback Loop")

    st.write("""
    Welcome to the Community Feedback Loop project, a platform aimed at gathering valuable insights and feedback from 
    users on various community projects. This feedback system allows project administrators to monitor user engagement, 
    gather user opinions, and improve project outcomes by understanding what resonates most with the community.
    
    Here, you can browse ongoing projects, submit feedback, and contribute to the community's shared growth. Administrators 
    can submit new projects and monitor feedback via an interactive dashboard, helping to shape future initiatives.
    """)

    if st.session_state.current_user is not None:
        st.write(f"Welcome, {st.session_state.current_user['username']}!")

        # CSS to make columns fit the content width
        st.markdown("""
            <style>
                div[data-testid="stColumn"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="stColumn"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

        # Create columns for closely aligned buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Submit Project", key="submit"):
                st.session_state.page = "submit_project"
                st.rerun()

        with col2:
            if st.session_state.current_user['is_admin']:
                if st.button("Dashboard", key="dashboard"):
                    st.session_state.page = "dashboard"
                    st.rerun()

        with col3:
            if st.button("Logout", key="logout"):
                logout()
                st.rerun()

    else:
        st.write("Please login to submit feedback. Use admin/admin or user/user for demo!")
        if st.button("Go to Login", key="login"):
            st.session_state.page = "login"
            st.rerun()

    st.header("Ongoing Projects")
    for _, project in st.session_state.projects.iterrows():
        st.subheader(project['title'])
        st.write(project['description'])
        if st.session_state.current_user is not None:
            if st.button(f"View Details (Project {project['id']})", key=f"view_{project['id']}"):
                st.session_state.current_project = project['id']
                st.session_state.page = "project_details"
                st.rerun()



def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_button"):
        if login(username, password):
            st.success("Logged in successfully!")
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid username or password")


def submit_project_page():
    st.title("Submit Project")
    st.write("### Enter details to submit a new project for community feedback.")

    title = st.text_input("Project Title")
    description = st.text_area("Project Description", placeholder="This project focuses on...")
    timeline = st.date_input("Timeline (Completion Date)")
    expected_impact = st.number_input("Expected Impact (e.g., expected reach or benefit level)", min_value=0, step=1)

    if st.button("Submit Project", key="submit_project_button"):
        new_project = pd.DataFrame([{
            'id': len(st.session_state.projects) + 1,
            'title': title,
            'description': description,
            'timeline': timeline.strftime("%Y-%m-%d"),
            'expected_impact': int(expected_impact)
        }])
        st.session_state.projects = pd.concat([st.session_state.projects, new_project], ignore_index=True)
        st.success("Project submitted successfully!")
        st.session_state.page = "home"
        st.rerun()


def project_details_page():
    project = st.session_state.projects[st.session_state.projects['id'] == st.session_state.current_project].iloc[0]
    st.title(project['title'])
    st.write(f"Description: {project['description']}")
    st.write(f"Timeline: {project['timeline']}")
    st.write(f"Expected Impact: {project['expected_impact']}")

    st.header("Submit Feedback")
    rating = st.slider("Rating", 1, 5, 3)
    comment = st.text_area("Comment")
    if st.button("Submit Feedback", key="submit_feedback_button"):
        new_feedback = pd.DataFrame([{
            'project_id': project['id'],
            'username': st.session_state.current_user['username'],
            'rating': rating,
            'comment': comment
        }])
        st.session_state.feedback = pd.concat([st.session_state.feedback, new_feedback], ignore_index=True)
        st.success("Feedback submitted successfully!")

    st.header("Feedback")
    project_feedback = st.session_state.feedback[st.session_state.feedback['project_id'] == project['id']]
    for _, feedback in project_feedback.iterrows():
        st.write(f"User: {feedback['username']}")
        st.write(f"Rating: {feedback['rating']}/5")
        st.write(f"Comment: {feedback['comment']}")
        st.write("---")


def dashboard_page():
    st.title("Dashboard")
    st.write("### Overview of Projects and Feedback")
    st.write("""
    This dashboard provides a quick overview of all projects and the feedback received for each. 
    Project metrics, such as average rating and total feedback count, are displayed to help administrators 
    assess engagement and make data-driven decisions.
    """)

    for _, project in st.session_state.projects.iterrows():
        with st.container():
            st.markdown(f"#### {project['title']}")
            st.write(f"*Description*: {project['description']}")
            st.write(f"*Timeline*: {project['timeline']}")
            st.write(f"*Expected Impact*: {project['expected_impact']}")

            project_feedback = st.session_state.feedback[st.session_state.feedback['project_id'] == project['id']]
            avg_rating = project_feedback['rating'].mean() if not project_feedback.empty else 0
            feedback_count = len(project_feedback)

            # Display project metrics in a card-like format
            col1, col2 = st.columns(2)
            col1.metric("Average Rating", f"{avg_rating:.2f}/5")
            col2.metric("Number of Feedbacks", feedback_count)

            st.divider()


# Main app logic
def main():
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home", key="home_button"):
        st.session_state.page = "home"
    if st.session_state.current_user is None:
        if st.sidebar.button("Login", key="login_sidebar"):
            st.session_state.page = "login"
    else:
        if st.session_state.current_user['is_admin']:
            if st.sidebar.button("Submit Project", key="submit_project_sidebar"):
                st.session_state.page = "submit_project"
            if st.sidebar.button("Dashboard", key="dashboard_sidebar"):
                st.session_state.page = "dashboard"

    if 'page' not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "submit_project":
        submit_project_page()
    elif st.session_state.page == "project_details":
        project_details_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()


if __name__ == "__main__":
    main()
