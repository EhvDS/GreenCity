import pandas as pd
import streamlit as st

if 'users' not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=['username', 'email', 'password', 'is_admin'])

    # Create data for the admin user
    admin_user = pd.DataFrame([{
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'admin',
        'is_admin': True
    }])

    st.session_state.users = pd.concat([st.session_state.users, admin_user], ignore_index=True)

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


# Page functions
def home_page():
    st.title("Community Feedback Loop")

    if st.session_state.current_user is not None:
        st.write(f"Welcome, {st.session_state.current_user['username']}!")
        if st.button("Logout"):
            logout()
            st.rerun()
    else:
        st.write("Please login to submit feedback. The credentials for the default test account are admin/admin!")
        if st.button("Go to Login"):
            st.session_state.page = "login"
            st.rerun()

    st.header("Ongoing Projects")
    for _, project in st.session_state.projects.iterrows():
        st.subheader(project['title'])
        st.write(project['description'])
        if st.session_state.current_user is not None:
            if st.button(f"View Details (Project {project['id']})"):
                st.session_state.current_project = project['id']
                st.session_state.page = "project_details"
                st.rerun()


def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login"):
        if login(username, password):
            st.success("Logged in successfully!")
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid username or password")


def submit_project_page():
    st.title("Submit Project")
    title = st.text_input("Project Title")
    description = st.text_area("Description")
    timeline = st.text_input("Timeline")
    expected_impact = st.text_area("Expected Impact")
    if st.button("Submit Project", key="submit_project"):
        new_project = pd.DataFrame([{
            'id': len(st.session_state.projects) + 1,
            'title': title,
            'description': description,
            'timeline': timeline,
            'expected_impact': expected_impact}])
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
    if st.button("Submit Feedback"):
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
    for _, project in st.session_state.projects.iterrows():
        st.subheader(project['title'])
        project_feedback = st.session_state.feedback[st.session_state.feedback['project_id'] == project['id']]
        avg_rating = project_feedback['rating'].mean() if not project_feedback.empty else 0
        st.write(f"Average Rating: {avg_rating:.2f}/5")
        st.write(f"Number of Feedbacks: {len(project_feedback)}")
        st.write("---")


# Main app logic
def main():
    st.sidebar.title("Navigation")
    if st.session_state.current_user is None:
        if st.sidebar.button("Home"):
            st.session_state.page = "home"
        if st.sidebar.button("Login"):
            st.session_state.page = "login"
    else:
        if st.sidebar.button("Home"):
            st.session_state.page = "home"
        if st.session_state.current_user['is_admin']:
            if st.sidebar.button("Submit Project"):
                st.session_state.page = "submit_project"
            if st.sidebar.button("Dashboard"):
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
