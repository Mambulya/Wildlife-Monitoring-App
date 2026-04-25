from ultralytics import YOLO

model_file = "app/models/best8n.pt"

def load_model() -> YOLO:
    """
    Loads the YOLO model from disk and saves it.
    returns: 
        model: YOLO - the loaded model
    """
    model = YOLO(model_file)
    return model