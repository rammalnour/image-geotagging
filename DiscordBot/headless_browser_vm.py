from time import sleep
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")


path = "/home/nferet/tests/img.png"


def GetRepIA(path):
    """
    - path : String

    Crée un browser en mode headless ( sans interface graphique)
    charge la page et upload l'image située au chemin path
    renvoie la liste contenant les probas de chaque région

    """
    def toFloat(String):
        if "e" in String:
            return 0
        return float(String)
    url = "https://geoimage.000webhostapp.com/AI.html"
    driver = webdriver.Firefox(options=options)
    print("driver created")
    driver.get(url)
    print("url fetched")
    y = driver.execute_script("return res.toString();")
    print("y=", y)
    sleep(1)
    input_element = driver.find_element(by="id", value='IAImage')
    input_element.send_keys(path)
    sleep(1)
    button_element = driver.find_element(by="id", value='startIaButton')
    button_element.click()
    x = driver.execute_script("return res.toString();")
    while x == "[object Promise]":
        x = driver.execute_script("return res.toString();")
        sleep(1)
    print(x)
    x = str(x)
    Lreps = x.split("[")[2][:-3]
    Lreps = Lreps.split(",")
    L = [toFloat(x) for x in Lreps]
    print(L)
    return L

#TESTS
assert len(L)==12
assert x != None
