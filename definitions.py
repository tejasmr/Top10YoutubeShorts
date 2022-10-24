from selenium.webdriver.common.by import By

TAG_NAME = By.TAG_NAME
CLASS_NAME = By.CLASS_NAME
XPATH = By.XPATH
ID = By.ID
CSS_SELECTOR = By.CSS_SELECTOR

class Category():
    def __init__(self, label):
        self.link = f"https://www.youtube.com/results?search_query=%23shorts+{label.lower()}&sp=CAMSBAgCEAE%253D"
        self.file = f"{label}_final.mp4"
        self.label = label

categories = []

def add(cat):
    categories.append(cat)

add("Finance")
add("Fitness")
add("Dance")
add("Gaming")
add("Streaming")
add("Movies")