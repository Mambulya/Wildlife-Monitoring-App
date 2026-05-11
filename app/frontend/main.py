import streamlit as st

############## constants ###############
HOME_PAGE_PATH = "pages/home.py"
GRAPHS_PAGE_PATH = "pages/graphs.py"
# HOME_PAGE_PATH = "app/frontend/pages/home_rus.py"     # rus version
URL_DETECT = "http://backend:8000/detect/"
URL_STATS = "http://backend:8000/stats/"
# URL_STATS = "http://localhost:8000/stats/"            # local running
# URL_DETECT = "http://localhost:8000/detect/"
HEADER_COLOR = "#9FB878"
ICON_PATH = "app/frontend/logo/app icon.png"
ICON_TREND_LOGO = "app/frontend/logo/trend_logo.png"
ICON_SIDEBAR_LOGO = "app/frontend/logo/sidebar_logo.png"
EMPTY_FOLDER_LOGO = "app/frontend/logo/empty_folder.png"

########################################

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon=ICON_PATH)


    pg = st.navigation(
        [
            st.Page(
                page=HOME_PAGE_PATH,
                title="Home | Upload photos",
                icon=":material/add:",
                default=True,
            ),
            st.Page(page=GRAPHS_PAGE_PATH, title="Statistical graphs", icon=":material/monitoring:"),
        ]
    )
    pg.run()