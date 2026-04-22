
classes_path = "../models/classes.txt"

def load_classes() -> str:
    """
    Loads the classes from disk and saves it.
    
    :returns: classes_str: str - the loaded classes as a string
    """
    with open(classes_path, "r") as f:
        classes_str = f.read()
    return classes_str