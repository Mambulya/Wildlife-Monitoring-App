import streamlit as st
import requests

from main import HEADER_COLOR, ICON_PATH, EMPTY_FOLDER_LOGO
from cache_loader import CacheLoader


def show_empty_logo():
    col_logo1= st.columns(vertical_alignment="center")
    with col_logo1:
        st.image(f"{EMPTY_FOLDER_LOGO}", width=400)

    col_logo2= st.columns(vertical_alignment="center")
    with col_logo2:
            st.write("""<div style='text-align: center; 
                            color: #575b5870; 
                            font-size: 60px;'>
            <strong>There are not any statistics yet.
            <br>Please, upload photos.</br></strong>
            </div>
            """, unsafe_allow_html=True)


############## UI Layout ##############
st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon=ICON_PATH)
st.markdown(f"""<h1 style='text-align: left; color: {HEADER_COLOR}; margin-bottom: 20px;'>
            Camera Trap Statisitcs</h1>""", unsafe_allow_html=True)
st.markdown(f"""
            <p style='text-align: left; font-size: 25px;'>
            There are graphs and diagrams illustrating statistics, which was discovered by cameras photos that have been just uploaded.
            All these diagrams can be helpful for Wildlife Monitoring.</p>
            """, unsafe_allow_html=True)



### metrics ###

if "file_names" in st.session_state:
    cache = CacheLoader(st.session_state.file_names) 

    if cache.get_status() == 200:
        all_stats = cache.get_dict()
        unique_species = cache.get_unique_species()
        total_uniq_species_num = cache.get_unique_species_number()
        species_population = cache.get_species_count()
        total_beings = cache.get_total_animals_count()
        top_species = cache.get_top(top=2)
        av_species_population = cache.get_av_species_frequency()
        empty_img_num = cache.get_empty_img()
        top_communal_species = cache.get_communal_top(3)

        st.write(str(all_stats))
        st.write(unique_species)
        st.write(total_uniq_species_num)
        st.write(species_population)
        st.write(total_beings)
        st.write(str(top_species))
        st.write(av_species_population)
        st.write(cache.num_img)
        st.write(empty_img_num)
        st.write(str(top_communal_species))



        col1, col2, col3, col4 = st.columns(4)


    else:
        show_empty_logo()

######################################



##### sidebar section #####
###########################