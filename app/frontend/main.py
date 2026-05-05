import streamlit as st

############## constants ###############
ICON_PATH = "app/frontend/logo/app icon.png"
HOME_PAGE_PATH = "pages/home.py"
# HOME_PAGE_PATH = "app/frontend/pages/home_rus.py"     # rus version
GRAPHS_PAGE_PATH = "pages/graphs.py"

########################################


st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon=ICON_PATH)


pg = st.navigation(
    [
        st.Page(
            page=HOME_PAGE_PATH,
            title="Home",
            icon="📷",
            default=True,
        ),
        st.Page(page=GRAPHS_PAGE_PATH, title="Camera traps photos graphs", icon="📊"),
    ]
)
pg.run()