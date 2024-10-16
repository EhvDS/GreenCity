import streamlit as st

# MAIN
def main():
    st.set_page_config(
        page_title='Interactive Tools for Sustainable Cities' ,
        page_icon='',   
        layout="wide",
        initial_sidebar_state="expanded")

    st.title("Interactive Tools for Sustainable Cities")
    st.sidebar.success("Choose ^^^")

    st.markdown("We set out to investigate how digital tools could help improve \
                (cooperative) decision-making in urban environments by offering accessible \
                information and inspiration. \
                This collection of proof-of-concept ideas explores different approaches: data visualization, \
                gamification, chatbots, augmented reality etc. All interactive and sometimes even fun!\
                Choose on the sidebar which one you want to try.")
    
    st.markdown("**Work in progress** by students of the Applied IT Master, [Fontys ICT](https://www.fontysictinnovationlab.nl/) .\
                All data and code is [available](https://github.com/EhvDS/GreenCity_app) but not yet properly reviewed and checked. \
                So :red[please don't base any serious conclusions on these proof-of-concepts yet].")

    st.markdown("Send your questions and comments to Simona Orzan ([s.orzan@fontys.nl](mailto:s.orzan@fontys.nl)).")

    st.markdown("Enjoy!")

if __name__ == '__main__':
    main()
