import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

def test_dobby_assistant(driver):
    driver.get("https://www.guvi.in/")
    wait = WebDriverWait(driver, 20)

    # Just find the Dobby button by ID
    dobby_button = wait.until(
        EC.presence_of_element_located((By.ID,"chatDetails"))
    )
    print("Found Dobby button in DOM")

    #  Click it using JS (works even if hidden)
    driver.execute_script("arguments[0].click();", dobby_button)
    print("Clicked Dobby button")

    # Verify chat window exists
    chat = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "ymMainContainer"))
    )
    assert chat is not None
    print("Dobby chat window opened")
