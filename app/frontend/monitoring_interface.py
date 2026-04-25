import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import time
import io
import zipfile
from PIL import Image

############## constants ###############

URL_DETECT = "http://backend:8000/detect/"
HEADER_COLOR = "#9FB878"
MAP_WIDTH = 400
MAP_HEIGHT = 300
PREVIEW_WIDTH = 700
HOME_LOGO_PATH = "app/frontend/logo/paws.png"
ICON_PATH = "app/frontend/logo/app icon.png"

if "submitted" not in st.session_state:
    st.session_state.submitted = False

########################################

def detect_images(uploaded_files):
    """
    Process uploaded images and send them to the backend API for detection.

    :param uploaded_files: List of uploaded image files

    :returns: content of the resulted zip-archive or None in the case of error
    """

    st.session_state.submitted = True

    start_time = time.time()
    bar = st.sidebar.progress(value=0)
    status_text = st.sidebar.empty()

    status_text.text("Processing images...")
    bar.progress(value=10)

    all_files = []
    for file in uploaded_files:
        file_bytes = file.getvalue()
        all_files.append(("files", (file.name, file_bytes, file.type)))
    try:
        response = requests.post(URL_DETECT, files=all_files, timeout=300)
        if response.status_code == 200:
            st.sidebar.success(f"Successfully processed all files!")
            st.sidebar.download_button(label="Download zip", 
                                data=response.content, 
                                file_name="detection.zip", 
                                mime="application/zip")
            end_time = time.time()
            bar.progress(value=100, text=f"Finished in {end_time - start_time:.2f} seconds")
            status_text.text(f"Finished in {end_time - start_time:.2f} seconds")
            bar.empty()
            return response.content
        else:
            st.sidebar.error(f"Failed to process: status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"An error occurred: {e}")

    bar.progress(value=100, text="Not finished")
    bar.empty()

    return None


def get_detected_img(zip_content: bytes):
    """
    Unpacks the zip file returned by the API and displays the initial and detected images side by side.
   
    :param zip_content: The content of the zip file returned by the API, containing detected images and label files.

    :returns: A dictionary with name of image and the detected image data itself
    """
    zip_bytes = io.BytesIO(zip_content)

    with zipfile.ZipFile(zip_bytes, 'r') as zip_file:
        files_list = zip_file.namelist()

        detected_img = dict()

        for file_name in files_list:
            if file_name.startswith("images/"):
                file_index = file_name[7:].split(".")[0]
                detected_img[file_index] = zip_file.read(file_name)

    return detected_img


def show_logo():
    col_logo1, col_logo2= st.columns([0.5,0.5], vertical_alignment="center")
    with col_logo1:
        st.image(f"{HOME_LOGO_PATH}", width=400)

    st.write("""<div style='text-align: center; 
                            color: #575b5870; 
                            font-size: 60px;'>
            <strong>Upload your trap-cameras' photos
            <br>to detect wild animals</br></strong>
            </div>
            """, unsafe_allow_html=True)

    col_logo1, col_logo2= st.columns([0.7,0.3], vertical_alignment="bottom")
    with col_logo2:
        st.image(f"{HOME_LOGO_PATH}", width=400)

############## UI Layout ##############
st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon=ICON_PATH)

st.markdown(f"""<h1 style='text-align: left; color: {HEADER_COLOR}; margin-bottom: 20px;'>
            Wildlife Monitoring App</h1>""", unsafe_allow_html=True)
col1, col2 = st.columns([0.3, 0.7], gap="medium")

with col1:
    reserve_map = folium.Map(location=[55.678609, 49.220126], zoom_start=8)
    folium.Marker([55.901026, 48.733690],
                  popup="Раифский участок", tooltip="Раифский участок").add_to(reserve_map)
    folium.Marker([55.302510, 49.273132], 
                  popup="Саралинский участок", tooltip="Саралинский участок").add_to(reserve_map)
    st_data = st_folium(reserve_map, width=MAP_WIDTH, height=MAP_HEIGHT)

with col2:
    # st.markdown("<h3 style='text-align: center;'>Detect wild animals from camera trap photos</h3>", unsafe_allow_html=True)
    st.markdown("#### Detect wild animals from Volgo-Kama Nature Reserve")
    col2.markdown("""<div style="text-align: justify;">
                    Environmental monitoring is considered a significant process of wildlife research in various territories. \
                    One of the places of active use may be <strong>Volzhsko-Kamsky Nature Reserve</strong>, founded in the republic \
                    Tatarstan was founded on April 13, 1960, and is an ecological, educational, environmental protection, and scientific research institution.  The
                    zone is designed to preserve the unique natural landscapes of the ancient Volga Valley. Since 2005, the reserve has been part of the \
                    UNESCO Biosphere Reserves. The reserve is located on the territory of the Republic of Tatarstan and consists of two sections: the Raifa  \
                  (area 5,921 ha) in Zelenodolsk district of the republic and Saralinsky (area 5,456 ha) in Laishevsky district.
                    <br>With regard to flora and fauna, 90% of the territories are covered with forests. The reserve is home to more than 50 species of mammals: white hare,
                    lynx, moose, yellow-throated mouse, hare hare, reddish ground squirrel, field mouse and others. Of the insectivores, you can often see a hedgehog, \
                    the mole and the common shrew. While there are more taiga fauna elements in the Raifa area, there are more forest–steppe elements in the Svralovsky area.
                  </div>
                  """, unsafe_allow_html=True)

st.markdown("---")

### graphs tests ###
# st.image("/Users/anyayashnova/Documents/obsidian_stuff/диплом/media/for_report_presentation/latency_accuracy_COCO-Object-Detection_mAPat50to95.png", use_container_width=True)  

##### sidebar section #####
st.sidebar.header("Upload Your Photos")
st.sidebar.write("Please, choose photos to detect wild animals")

with st.sidebar.expander("Image Guidelines"):
    st.write("""
    - Maximum 100 images per upload
    - Supported formats: PNG, JPG, JPEG
    - The zip archive returned by the API will contain:
        - Detected images with bounding boxes in the `images/` folder
        - Corresponding label files in the `labels/` folder
    - For detection YOLO8n model is used
    - Each label file will contain the detected classes and their coordinates in YOLO format
    """)

uploaded_files = st.sidebar.file_uploader("Upload Files", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

#########################################


############## Main Logic ##############
if len(uploaded_files) != 0:

    if st.sidebar.button("Submit"):
        st.session_state.submitted = True

        zip_archive = detect_images(uploaded_files)             # operating and downloading results
        if zip_archive is not None:
            detected_images = get_detected_img(zip_archive)

            ##### results preview #####
            col_preview_1, col_preview_2 = st.columns([0.5, 0.5], gap="xsmall", vertical_alignment="center")
            col_preview_1.write("Initial Image")
            col_preview_2.write("Detected Image")

            for file in uploaded_files:
                file_name = file.name.split(".", 1)[0]

                with col_preview_1:
                    st.image(image=file, width=PREVIEW_WIDTH)

                with col_preview_2:
                    res_img = Image.open(io.BytesIO(detected_images[file_name]))
                    st.image(image = res_img, width=PREVIEW_WIDTH)
            st.markdown("If you are satisfied with results, you can download it by the __Download zip__ left.")
            st.write("""
            The zip archive returned by the API will contain:
            - Detected images with bounding boxes in the `images/` folder.
            - Corresponding label files in the `labels/` folder.
            """)
    else:
        show_logo()
else:
    show_logo()


########## running #################
# before running UI make sure that the backend FAST API is running on URL_DETECTION
# for this you need to run the main.py file from backend folder, and then you can run this UI script.
# 
# python3 ../backend/main.py                <- run the backend API
# cd ../frontend
# streamlit run monitoring_interface.py     <- run the UI interface
