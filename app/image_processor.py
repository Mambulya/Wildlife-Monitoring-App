import cv2
import numpy as np
from ultralytics import YOLO



def image_process_with_YOLO(img: bytes, model: YOLO) -> bytes:
    """
    Process an image with YOLO detector.

    :param img: Byted image.
    :param model: YOLO detector.

    :returns: a detected image as bytes with its meta-data label file.
    """
    # bytes -> OpenCV BGR image 
    img_arr = np.frombuffer(buffer=img, dtype=np.uint8)
    image = cv2.imdecode(buf=img_arr, flags=cv2.IMREAD_COLOR)

    preds = model(image)

    # bounding box
    annotation = preds[0].plot()

    # Results -> jpg (small memery usage)
    success, encoded_bytes = cv2.imencode(ext=".jpg", img=annotation)
    print("SUCCESS:", success)
    if success:
        return encoded_bytes
    return Exception("Enconding was failed")
