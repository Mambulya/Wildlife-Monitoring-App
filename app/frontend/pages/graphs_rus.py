import streamlit as st
from streamlit_echarts import st_echarts
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd

from main import HEADER_COLOR, ICON_PATH, EMPTY_FOLDER_LOGO, ICON_SIDEBAR_LOGO
from cache_loader import CacheLoader

FONT_SIZE = 20


def show_empty_logo():
    col_logo1= st.columns([1], vertical_alignment="center")[0]
    with col_logo1:
            st.write("""<div style='text-align: center; 
                            color: #575b5870; 
                            margin-top: 50px;
                            margin-bottom: 10px;
                            font-size: 60px;'>
            <strong>Здесть пока что нет никакой статистики.
            <br>Пожалуйста, загрусити фотографии.</br></strong>
            </div>
            """, unsafe_allow_html=True)    

    col_logo2, col_logo3, col_logo4= st.columns([0.33, 0.33, 0.33], vertical_alignment="center")
    with col_logo3:
        st.image(f"{EMPTY_FOLDER_LOGO}", width=400)


############## UI Layout ##############
st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon=ICON_PATH)
st.markdown(f"""<h1 style='text-align: left; color: {HEADER_COLOR}; margin-bottom: 20px;'>
            Статистика по снимкам из фотоловушки</h1>""", unsafe_allow_html=True)

##### sidebar #####
st.sidebar.header("Статистика из загруженных снимков")
st.sidebar.write("Здесь можно найти статистическую информацию после загрузки снимков.")
# st.sidebar.image(image=ICON_SIDEBAR_LOGO)
st.sidebar.write("""<strong><p style='text-align: center;'>
                 Исследуйте, анализируйте и сохраняйте!</p></strong>
                 """, unsafe_allow_html=True)
###################

### metrics ###

if "file_names" in st.session_state:
    cache = CacheLoader(st.session_state.file_names) 

    if cache.get_status() == 200:
        st.markdown(f"""
            <p style='text-align: left; font-size: {FONT_SIZE}px;'>
            Здесь распогалагются статистическоие графики и диаграммы, которые являются результатом анализа снимков, которые вы только что загрузили.
            Все материалы могут помочь в мониторинге дикой природы.</p>
            """, unsafe_allow_html=True)
        all_stats = cache.get_dict()
        unique_species = cache.get_unique_species()
        total_uniq_species_num = cache.get_unique_species_number()
        species_population = cache.get_species_count()
        total_beings = cache.get_total_animals_count()

        if total_uniq_species_num >= 3:
            top_species = cache.get_top(top=3)
        else:
            top_species = cache.get_top(top=total_uniq_species_num)

        av_species_population = cache.get_av_species_frequency()
        empty_img_num = cache.get_empty_img()

        if total_uniq_species_num >= 3:
            top_communal_species = cache.get_communal_top(3)
        else:
            top_communal_species = cache.get_communal_top(top=total_uniq_species_num)

        all_img_num = cache.num_img
        empty_img_num = cache.get_empty_img()
        
        # st.write(str(all_stats))
        # st.write(unique_species)
        # st.write(total_uniq_species_num)
        # st.write(species_population)
        # st.write(total_beings)
        # st.write(str(top_species))
        # st.write(av_species_population)
        # st.write(cache.num_img)
        # st.write(empty_img_num)
        # st.write(str(top_communal_species))

        # ---- metrics ----

        col0, col1, col2, col3, col4, col5 = st.columns([0.05, 0.25, 0.25, 0.25, 0.25, 0.05], vertical_alignment="center")

        if total_beings > 0:
            with col1: 
                st.metric(
                    label="Всего было обнаружено",
                    value=f"{total_beings} особей",
                    border=False,
                    height="stretch"
                )
            with col2:
                st.metric(
                    label=f"__{top_species[0][0].capitalize()}__ особей из них",
                    value=f"{top_species[0][1]}",
                    border=True,
                    delta="Top 1",
                    delta_color="green",
                    delta_arrow="off"
                    )
            if len(top_species) > 1:
                with col3:
                    st.metric(
                        label=f"__{top_species[1][0].capitalize()}__ особей из них",
                        value=f"{top_species[1][1]}",
                        border=True,
                        delta="Top 2",
                        delta_color="green",
                        delta_arrow="off"
                      )
                if len(top_species) > 2:
                    with col4:
                        st.metric(
                            label=f"__{top_species[2][0].capitalize()}__ особей из них",
                            value=f"{top_species[2][1]}",
                            border=True,
                            delta="Top 3",
                            delta_color="green",
                            delta_arrow="off"
                        )
        st.markdown("<p style='margin-bottom: 20px;'> </p>", unsafe_allow_html=True)
                
        # ---- animals detection diagrams ----    
        st.subheader("Распределение видов и Социальное поведение")
        st.markdown(f"""<p style='text-align: left; font-size: {FONT_SIZE}px; margin-bottom: 20px;'>
                    Ниже находится инфоррмация о распределении различных видов за одну операцию детекции, так же как и данные
                    о распределении размера группы животных относительно вида, показывающие, имеет ли животное солитарные или 
                    социальные признаки поведения. 
                    </p>
                    """, unsafe_allow_html=True)

        col6, col7 = st.columns(spec=[0.6, 0.4], vertical_alignment="center")


        # ---- bar chart for Group Size Distribution ----   
        with col6:

            group_size_opts = {
                "title": {
                    "text": "Среднее количество особей за детекцию", 
                    "left": "center"
                          },
                "toolbox": {
                    "feature": {
                        "saveAsImage": {}
                    }
                },
                "legend": {
                    "bottom": "0", 
                    "type": "scroll", 
                    "textStyle": {"fontSize": 10}
                           },
                "tooltip": {
                    "trigger": "axis", 
                    "axisPointer": {"type": "shadow"},
                    "formatter": "{b}: в среднем {c} особей на фото"
                            },
                "grid": {
                    "left": "3%",
                    "right": "4%",
                    "bottom": "15%",
                    "containLabel": True,
                            },
                "xAxis": {
                    "type":"value",
                    # "name": "Mean group size",
                            },
                "yAxis": {
                    "type": "category", 
                    "data": list(av_species_population.keys()),
                    # "name": "Species",
                    "axisLabel": {
                        "fontSize": 16
                                }

                        },
                "series": [{"data": list(av_species_population.values()), 
                            "type":"bar",
                            "itemStyle": {
                                "color": HEADER_COLOR
                            }
                            }]
            }
    
            st_echarts(options=group_size_opts, height="450px", key="Среднее количество животных за детекцию")
        
        
        # ---- pie chart for species Distribution ----
        with col7:
            donut_opts = {
                "color": [mcolors.to_hex(plt.cm.ocean(i / total_uniq_species_num)) for i in range(total_uniq_species_num)],
                "title": {"text": "Распределение видов", 
                          "left": "center"},
                "toolbox": {
                    "feature": {
                        "saveAsImage": {}
                    }
                },
                "tooltip": {"trigger": "item", 
                            "formatter": "{b}: {c} beings ({d}%)"},
                            
                "series": [
                    {
                        "type": "pie",
                        "radius": ["40%", "70%"],
                        "avoidLabelOverlap": True,
                        "itemStyle": {
                            "borderRadius": 10,
                            "borderColor": "#fff",
                            "borderWidth": 2,
                    },
                "label": {"show": True, 
                          "formatter": "{b}: {d}%"},
                "emphasis": {
                        "label": {"show": True, "fontSize": "14", "fontWeight": "bold"},
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        },
                    },
                "data": [{"value": value, "name": key} for key, value in species_population.items()]
                    }
                ],
            }

            st_echarts(options=donut_opts, height="450px", key="priority_donut")

        st.markdown("<p style='margin-bottom: 20px;'> </p>", unsafe_allow_html=True)
        st.subheader("Пустые снимки")
        st.markdown(f"""<p style='text-align: left; font-size: {FONT_SIZE}px; margin-bottom: 50px;'>
                    Фотоловушки иногда склоны к ложным срабатываниям. Именно поэтому подобные девайсы создают и сохраняют
                    снимки, которые не отображают животных в принципе. Здесь представлено сравнение долей пустых снимков с
                    информативными.
                    </p>
                    """, unsafe_allow_html=True)
        
        col__, col8, col9, col_, col10 = st.columns([0.07, 0.17, 0.17, 0.07, 0.5], vertical_alignment="center", gap="small")

        with col8:
            st.metric(
                label="Снимки с животными",
                value=f"{((all_img_num - empty_img_num) / all_img_num * 100):,.2f}%",
                delta=f"{all_img_num - empty_img_num} снимков",
                delta_arrow="off",
                border=True,
                delta_color="green"
            )

        with col9:
            st.metric(
                label="Снимки без животных",
                value=f"{(empty_img_num / all_img_num * 100):,.2f}%",
                delta=f"{empty_img_num} снимков",
                delta_arrow="off",
                border=True,
                delta_color="red"
            )         

        with col10:
            df_temp = pd.DataFrame({"Label": [""], "Информативные снимки": [all_img_num - empty_img_num], "Пустые снимки": [empty_img_num]})
            st.bar_chart(data=df_temp, x="Label", y=["Информативные снимки", "Пустые снимки"], x_label="", y_label="Количество снимков", stack=False, color=[HEADER_COLOR, "#d75136"]) 
            del df_temp  

    else:
        st.error("Error with connection occured :(")
else:
     show_empty_logo()

######################################



##### sidebar section #####
###########################