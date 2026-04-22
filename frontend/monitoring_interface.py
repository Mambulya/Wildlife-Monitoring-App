import streamlit as st
import requests
import time

############## constants ###############

URL_DETECT = "http://127.0.0.1:8000/detect/"

########################################

def detect_images(uploaded_files):
    """
    Process uploaded images and send them to the backend API for detection.

    :param uploaded_files: List of uploaded image files
    """
    if st.sidebar.button("Submit"):

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
            else:
                st.sidebar.error(f"Failed to process: status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"An error occurred: {e}")

        end_time = time.time()
        bar.progress(value=100, text=f"Finished in {end_time - start_time:.2f} seconds")
        bar.empty()



############## UI Layout ##############
st.set_page_config(layout="wide", page_title="Wild Animals Detection App", page_icon="")
st.image("logo/reserve_log1.jpg", use_container_width=True )


st.title("Wildlife Monitoring App")
st.subheader('Detect wild animals from camera trap photos')
col1, col2 = st.columns(2)

st.write("The system can detect popular wild species, which habitat is concentrated in the Volga-Kama Reserve in Tatarstan republic, Russia, "\
         "such as wild boar, roe deer, moose, badger, fow, silver gull, and etc. \n" \
         "The detection is based on the YOLOv8 model, which is trained on a custom dataset of camera trap photos from the reserve.\n" \
         "The app allows you to upload your own photos and get the detected images with bounding boxes and corresponding label files in a zip archive for further monitoring goals."\
        )

##### sidebar section #####
st.sidebar.header("Upload Your Photos")
st.sidebar.write("Please, choose photos to detect wild animals")

with st.sidebar.expander("Image Guidelines"):
    st.write("""
    - MAximum 100 images per upload.
    - Supported formats: PNG, JPG, JPEG
    - The zip archive returned by the API will contain:
        - Detected images with bounding boxes in the `images/` folder.
        - Corresponding label files in the `labels/` folder.
    - Each label file will contain the detected classes and their coordinates in YOLO format.
    """)

uploaded_files = st.sidebar.file_uploader("Upload Files", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

#########################################


############## Main Logic ##############
if uploaded_files is not None:
    detect_images(uploaded_files)

else:
    st.info("Please upload images to detect wild animals")


########## running #################
# before running UI make sure that the backend FAST API is running on URL_DETECTION
# for this you need to run the main.py file from backend folder, and then you can run this UI script.
# 
# python3 ../backend/main.py                <- run the backend API
# streamlit run monitoring_interface.py     <- run the UI interface
