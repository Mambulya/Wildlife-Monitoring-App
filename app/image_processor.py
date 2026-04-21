import cv2
import numpy as np
from ultralytics import YOLO


def extract_label(preds: list) -> str:
    """
    Extract label from YOLO predictions 
    in the following format: class_id, x_center, y_center, width, height (not normalized).
    
    :param preds: YOLO predictions.

    :returns: a string of labels.
    """
    for pred in preds:
        labels_pred = []
        for box in pred.boxes:
            if box is None:
                continue
            else:
                cls_id = box.cls[0] 
                xywh = box.xywh[0]
                # confidence = box.conf            
                label = f"{cls_id} {xywh[0]} {xywh[1]} {xywh[2]} {xywh[3]}"
                labels_pred.append(label)

    label_file = "\n".join(labels_pred)
    return label_file


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
        label_file = extract_label(preds)
        return encoded_bytes, label_file
    return Exception("Enconding was failed")
