
classes_path = "app/models/classes.txt"

def load_classes() -> str:
    """
    Loads the classes from disk and saves it.
    
    :returns: classes_str: str - the loaded classes as a string
    """
    with open(classes_path, "r") as f:
        classes_str = f.read()
    return classes_str

def load_classes_list() -> list:
    """
    Loads the classes from disk and saves it as a list.
    
    :returns: classes_str: str - the loaded classes as a list
    """
    classes = []
    with open(classes_path, "r") as f:
        for line in f:
            classes.append(line.strip())
    return classes
        
